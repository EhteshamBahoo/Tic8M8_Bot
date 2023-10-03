### RELATIVE DATE DEMO SIMPLE PYTHON
from datetime import datetime, timedelta

class RelativeDate():
    def name(self):
        return "return_relative_date"


import spacy
from datetime import datetime, timedelta

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

def get_relative_date():
    while True:
        try:
            user_input = input("Enter a date expression (e.g., 'next month', 'next week', 'tomorrow', 'today'): ").strip().lower()

            # Get the current date
            current_date = datetime.now()

            # Process the user input using spaCy
            doc = nlp(user_input)

            # Interpret the date expression
            for token in doc:
                if token.text == "next" and token.head.text in ["month", "week"]:
                    if token.head.text == "month":
                        result_date = current_date + timedelta(days=30)
                    elif token.head.text == "week":
                        result_date = current_date + timedelta(weeks=1)
                    return result_date.strftime("%Y-%m-%d")
                elif token.text == "tomorrow":
                    result_date = current_date + timedelta(days=1)
                    return result_date.strftime("%Y-%m-%d")
                elif token.text == "today":
                    return current_date.strftime("%Y-%m-%d")

            print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input format. Please try again.")

if __name__ == "__main__":
    relative_date = get_relative_date()
    print("The calculated date is:", relative_date)
