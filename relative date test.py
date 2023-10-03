import spacy
from datetime import datetime, timedelta
import re
import requests

nlp = spacy.load("en_core_web_sm")

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
    match = re.search(r'(\d+)\s*(day|week|month)[s]*', text)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        
        delta_days = 0
        delta_weeks = 0
        delta_months = 0

        if unit == 'day':
            delta_days = amount
        elif unit == 'week':
            delta_weeks = amount
        elif unit == 'month':
            delta_months = amount
        
        current_date = datetime.now()
        result_date = current_date + timedelta(
            days=delta_days + delta_months * 30,
            weeks=delta_weeks
        )

        return result_date.strftime("%Y-%m-%d")
    
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
                return (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
            elif "next month" in user_input:
                return (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Try to extract date information from the text
            relative_date = extract_date_from_text(user_input)
            if relative_date:
                return relative_date

            print("Invalid input format. Please try again.")
        except ValueError:
            print("Invalid input format. Please try again.")

def fetch_events(start_date):
    api_url = "https://dev.tic8m8.com/api/getevents"
    
    params = {"startdate": start_date}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }
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
    print("The calculated date is:", relative_date)
    
    fetch_events(relative_date)
