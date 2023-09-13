import requests
import json

def get_events(city):
    base_url = "https://dev.tic8m8.com/api/getevents"
    query = {"q": json.dumps({"city": city})}

    # Define headers with your API key (if required)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}


    # Send a GET request to the API with the query parameter
    response = requests.get(base_url, headers=headers, params=query)

    if response.status_code == 200:
        events = response.json()
        return events
    else:
        print("Failed to fetch data from the API")
        return []

if __name__ == "__main__":
    user_input = input("Enter a city to list events happening there: ")
    events = get_events(user_input)

    if events:
        print(f"Events in {user_input}:")
        for events in events:
            print(events)
    else:
        print(f"No events found in {user_input}")
