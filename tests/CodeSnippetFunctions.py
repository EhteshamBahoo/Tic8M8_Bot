import requests
from typing import Dict, List, Any

class EventAPI:
    def __init__(self):
        self.base_url = "https://dev.tic8m8.com/api"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }

    def get_events_by_maxprice(self, max_price: float) -> List[Dict[str, Any]]:
        api_url = f"{self.base_url}/getevents"
        params = {"maxprice": max_price}
        
        response = requests.get(api_url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return []

def list_events_by_max_price(max_price: float) -> List[Dict[str, Any]]:
    event_api = EventAPI()
    return event_api.get_events_by_maxprice(max_price)

# Example usage:
if __name__ == "__main__":
    max_price = 200.0  # Replace with the desired maximum price
    events = list_events_by_max_price(max_price)

    if events:
        for event in events:
            event_name = event.get("event_name", "N/A")
            event_location = event.get("street", "N/A")
            print(f"Event: {event_name}, Location: {event_location}")
    else:
        print("No events found within the specified price range.")