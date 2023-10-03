### RELATIVE DATE DEMO SIMPLE PYTHON
from datetime import datetime, timedelta

class RelativeDate():
    def name(self):
        return "return_relative_date"



def get_relative_date():
    while True:
        try:
            user_input = input("Enter a relative date (next month/next week/tomorrow/today): ").strip().lower()

            # Get the current date
            current_date = datetime.now()

            if user_input == 'next month':
                result_date = current_date + timedelta(days=30)
            elif user_input == 'next week':
                result_date = current_date + timedelta(weeks=1)
            elif user_input == 'tomorrow':
                result_date = current_date + timedelta(days=1)
            elif user_input == 'today':
                result_date = current_date
            else:
                print("Invalid input. Please enter 'next month', 'next week', 'tomorrow', or 'today'.")
                continue

            return result_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid input format. Please try again.")

if __name__ == "__main__":
    relative_date = get_relative_date()
    print("The calculated date is:", relative_date)
