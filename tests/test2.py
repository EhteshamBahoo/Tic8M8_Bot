import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class CustomAction(Action):
    def __init__(self):
        self.base_url = "https://dev.tic8m8.com/api/getevents"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}

    def construct_api_url(self, api_function: Text, api_query: Text) -> Text:
        return f"{self.base_url}/{api_function}/{api_query}"

class ActionListEvents(CustomAction):
    def name(self) -> Text:
        return "action_list_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_category = tracker.get_slot("event_category")
        event_location = tracker.get_slot("event_location")
        event_price_range = tracker.get_slot("event_price_range")
        event_date = tracker.get_slot("event_date")
        event_artists = tracker.get_slot("event_artists")

        api_function = "getevent"
        api_query = f"?category={event_category}&location={event_location}&price_range={event_price_range}&date={event_date}&artists={event_artists}"
        api_url = self.construct_api_url(api_function, api_query)

        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            events = response.json()

            if events:
                event_list = "\n".join([event["name"] for event in events])
                dispatcher.utter_message(f"Here are the events that match your criteria:\n{event_list}")
                return [SlotSet("events_found", event_list)]  
            else:
                dispatcher.utter_message("I am so sorry I couldn't find any events that match your criteria, Do you wanna Try again?")
                return [SlotSet("events_found", None)]  
        else:
            dispatcher.utter_message("There was an issue fetching data from the API.")
            return []

print('hello world')
