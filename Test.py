import requests
from typing import (
    Any, Text, Dict, List
    )
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class EventAPI:
    def __init__(self):
        self.base_url = "https://dev.tic8m8.com/api"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }

    def get_events(self, params: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_url = f"{self.base_url}/getevents"
        response = requests.get(api_url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return []


class ListEventsAction(Action):
    def name(self) -> Text:
        return "action_list_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_api = EventAPI()
        
        event_city = tracker.get_slot("event_city")
        event_category = tracker.get_slot("event_category")
        ImageURL = "https://tic8m8.com/uploads/events/"

        if event_city and event_category:
            params = {"city": event_city, "category": event_category}
            events = event_api.get_events(params)
            if events:
                carousel_elements = []

                for event in events:
                    event_name = event.get('name', 'Event Name N/A')
                    event_city = f"{event_name} in {event_city}"
                    image_url = event.get(f'{ImageURL}image_name', '')

                    carousel_elements.append({
                        "title": event_name,
                        "subtitle": event_city,
                        "image_url": image_url,
                        "buttons": [
                            {
                                "title": "More Details",
                                "url": event.get('url', ''),
                                "type": "web_url"
                            }
                        ]
                    })

                message = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": carousel_elements
                    }
                }

                dispatcher.utter_message(attachment=message)
            else:
                dispatcher.utter_message(f"No events found in {event_city} in the {event_category} category.")
        else:
            dispatcher.utter_message("Please specify both a city and a category.")

        return []



# class ActionListCoursel(Action):
#     def name(self) -> Text:
#         return "action_carousels"
    
#     def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         message = {
#             "type": "template",
#             "payload": {
#                 "template_type": "generic",
#                 "elements": [
#                     {
#                         "title": "Global Village",
#                         "subtitle": "AED 25",
#                         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqhmyBRCngkU_OKSL6gBQxCSH-cufgmZwb2w&usqp=CAU",
#                         "buttons": [ 
#                             {
#                             "title": "Contact Information",
#                             "payload": "Contact Information",
#                             "type": "postback"
#                             },
#                             {
#                             "title": "More Info",
#                             "payload": "More Info",
#                             "type": "postback"
#                             }
#                         ]
#                     },
#                     {
#                         "title": "The Forex Expo Dubai",
#                         "subtitle": "free",
#                         "image_url": "https://tic8m8.com/uploads/events/64bdd270c1514354124634.png",
#                         "buttons": [ 
#                             {
#                             "title": "More Details",
#                             "url": "https://tic8m8.com/en/event/the-forex-expo-dubai",
#                             "type": "web_url"
#                             }
#                         ]
#                     }
#                 ]
#                 }
#         }
#         dispatcher.utter_message(attachment=message)
