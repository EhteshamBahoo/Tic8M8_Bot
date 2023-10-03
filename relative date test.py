import spacy
from datetime import datetime, timedelta

nlp = spacy.load("en_core_web_sm")

def get_relative_date():
    while True:
        try:
            user_input = input("Enter a date expression (e.g., 'next month', 'next week', 'tomorrow', 'today'): ").strip().lower()
            current_date = datetime.now()
            doc = nlp(user_input)

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

        except ValueError:
            print("Invalid input format. Please try again.")

if __name__ == "__main__":
    relative_date = get_relative_date()
    print("The calculated date is:", relative_date)
