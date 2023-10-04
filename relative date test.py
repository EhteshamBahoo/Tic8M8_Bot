import spacy
from datetime import datetime, timedelta
import re
import requests

nlp = spacy.load("en_core_web_sm")

MONTH_ABBREVIATIONS = {
    "jan": "january",
    "feb": "february",
    "mar": "march",
    "apr": "april",
    "may": "may",
    "jun": "june",
    "jul": "july",
    "aug": "august",
    "sep": "september",
    "oct": "october",
    "nov": "november",
    "dec": "december",
}

def parse_date_expression(text):
    current_date = datetime.now()
    doc = nlp(text)

    delta_days = 0
    delta_weeks = 0
    delta_months = 0

    for ent in doc.ents:
        if ent.label_ == "DATE":
            if "week" in ent.text:
                delta_weeks = int(ent.text.split()[0])
            elif "month" in ent.text:
                delta_months = int(ent.text.split()[0])
            elif "day" in ent.text:
                delta_days = int(ent.text.split()[0])

    result_date = current_date + timedelta(
        days=delta_days + delta_months * 30,
        weeks=delta_weeks
    )

    return result_date.strftime("%Y-%m-%d")

def extract_date_from_text(text):
    if "today" in text:
        return datetime.now().strftime("%Y-%m-%d")
    elif "tomorrow" in text:
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    month_match = re.search(r'(\b(january|february|march|april|may|june|july|august|september|october|november|december|'
                           r'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b)', text, re.IGNORECASE)
    
    if month_match:
        month_name = month_match.group(1).lower()
        
        full_month_name = MONTH_ABBREVIATIONS.get(month_name, month_name)
        
        current_year = datetime.now().year
        current_month = datetime.now().month
        month_start = datetime.strptime(f"{full_month_name} 1, {current_year}", "%B %d, %Y")
        
        if month_start.month < current_month:
            month_start = datetime.strptime(f"{full_month_name} 1, {current_year + 1}", "%B %d, %Y")
        
        month_end = (month_start.replace(day=1, month=month_start.month % 12 + 1) - timedelta(days=1)).replace(day=31)
        return month_start.strftime("%Y-%m-%d"), month_end.strftime("%Y-%m-%d")
    
    # Attempt to extract weekday information from the text
    weekday_match = re.search(r'\b(sunday|monday|tuesday|wednesday|thursday|friday|saturday)\b', text, re.IGNORECASE)
    
    if weekday_match:
        current_date = datetime.now()
        target_weekday = weekday_match.group(0).lower()
        days_until_weekday = (current_date.weekday() - ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(target_weekday)) % 7
        target_date = current_date + timedelta(days=days_until_weekday)
        return target_date.strftime("%Y-%m-%d"), target_date.strftime("%Y-%m-%d")  # Set both start and end date to the same day
    
    return None

def get_relative_date():
    while True:
        try:
            user_input = input("Enter a date expression (e.g., 'next month', 'next week', 'tomorrow', 'today'): ").strip().lower()

            # Check for common keywords
            if "today" in user_input:
                return datetime.now().strftime("%Y-%m-%d")
            elif "tomorrow" in user_input:
                return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            elif "next week" in user_input:
                # Calculate the date range for the upcoming week
                start_date = datetime.now() + timedelta(days=7 - datetime.now().weekday())
                end_date = start_date + timedelta(days=6)
                return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
            elif "next month" in user_input:
                return (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            elif "next" in user_input:
                # Handle "next" followed by a day of the week
                weekday_match = re.search(r'\b(sunday|monday|tuesday|wednesday|thursday|friday|saturday)\b', user_input, re.IGNORECASE)
                if weekday_match:
                    current_date = datetime.now()
                    target_weekday = weekday_match.group(0).lower()
                    days_until_weekday = (current_date.weekday() - ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(target_weekday)) % 7
                    target_date = current_date + timedelta(days=days_until_weekday + 7)  # Add 7 days to get the next occurrence
                    return target_date.strftime("%Y-%m-%d"), target_date.strftime("%Y-%m-%d")  # Set both start and end date to the same day
            
            # Try to extract date information from the text
            date_range = extract_date_from_text(user_input)
            if date_range:
                if isinstance(date_range, tuple):
                    start_date, end_date = date_range
                    print(f"The date range is from {start_date} to {end_date}")
                    return start_date, end_date
                else:
                    return date_range

            print("Invalid input format. Please try again.")
        except ValueError:
            print("Invalid input format. Please try again.")

def fetch_events(start_date, end_date=None):
    api_url = "https://dev.tic8m8.com/api/getevents"
    
    params = {"dateRangeStart": start_date}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }
    if end_date:
        params["dateRangeEnd"] = end_date
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            events = data if isinstance(data, list) else []

            if not events:
                print("No events found for the given date.")
                return

            for event in events:
                event_name = event.get("event_name", "N/A")
                street = event.get("street", "N/A")
                print("Event Name:", event_name)
                print("Street:", street)
                print()
        else:
            print(f"Failed to fetch events. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    relative_date = get_relative_date()
    
    if isinstance(relative_date, tuple):
        start_date, end_date = relative_date
        fetch_events(start_date, end_date)
    else:
        fetch_events(relative_date)
