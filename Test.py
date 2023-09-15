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

            

class ActionListAllEvents(Action):
    def name(self) -> Text:
        return "action_list_all_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_city = tracker.get_slot("event_city")
        event_artists = tracker.get_slot("event_artists")
        event_date = tracker.get_slot("event_date")
        event_category = tracker.get_slot("event_category")

        params = {
            "city": event_city or "",  
            "artists": event_artists or "",
            "startdate": event_date or "",
            "category": event_category or ""
        }

        event_api = EventAPI()
        events = event_api.get_events(params)

        if events:
            event_list = []
            for event in events:
                event_name = event.get("event_name", "N/A")
                event_location = event.get("street", "N/A")
                image_name = event.get("image_name", "N/A")
                externallink = event.get("externallink", "N/A")

                event_info = f"Event Name: {event_name}\nLocation: {event_location}\nImage: {image_name}\nLink: {externallink}\n"
                event_list.append(event_info)

            response_message = "Here is the list of events:\n\n" + "\n".join(event_list)
            dispatcher.utter_message(response_message)
        else:
            dispatcher.utter_message("I couldn't find any events matching your criteria.")

        return []



#####################


class ActionListCoursel(Action):
    def name(self) -> Text:
        return "action_carousels"
    
    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Global Village",
                        "subtitle": "AED 25",
                        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqhmyBRCngkU_OKSL6gBQxCSH-cufgmZwb2w&usqp=CAU",
                        "buttons": [ 
                            {
                            "title": "Contact Information",
                            "payload": "Contact Information",
                            "type": "postback"
                            },
                            {
                            "title": "More Info",
                            "payload": "More Info",
                            "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "The Forex Expo Dubai",
                        "subtitle": "free",
                        "image_url": "https://tic8m8.com/uploads/events/64bdd270c1514354124634.png",
                        "buttons": [ 
                            {
                            "title": "More Details",
                            "url": "https://tic8m8.com/en/event/the-forex-expo-dubai",
                            "type": "web_url"
                            }
                        ]
                    }
                ]
                }
        }
        dispatcher.utter_message(attachment=message)


class ActionListAllEvents(Action):
    def name(self) -> Text:
        return "action_list_all_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_city = tracker.get_slot("event_city")
        event_artists = tracker.get_slot("event_artists")
        event_date = tracker.get_slot("event_date")
        event_category = tracker.get_slot("event_category")

        params = {
            "city": event_city or "",  
            "artists": event_artists or "",
            "startdate": event_date or "",
            "category": event_category or ""
        }

        event_api = EventAPI()
        events = event_api.get_events(params)
        if events:
            event_list = []
            for event in events:
                event_name = event.get("event_name", "N/A")
                event_location = event.get("street", "N/A")
                image_name = event.get("image_name", "N/A")
                externallink = event.get("externallink", "N/A")

                # event_info = f"Event Name: {event_name}\nLocation: {event_location}\nImage: {image_name}\nLink: {externallink}\n"
                # event_list.append(event_info)
                message = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": event_name,
                                "subtitle": event_location,
                                "image_url": f"https://tic8m8.com/uploads/events/{image_name}",
                                "buttons": [ 
                                    {
                                    "title": "Contact Information",
                                    "payload": f"Contact Information for {event_name}",
                                    "type": "postback"
                                    },
                                    {
                                    "title": "More Info",
                                    "payload": f"More Information of {event_name}",
                                    "type": "postback"
                                    }
                                ]
                            },
                            {
                                "title": "The Forex Expo Dubai",
                                "subtitle": "free",
                                "image_url": f"https://tic8m8.com/uploads/events/{image_name}",
                                "buttons": [ 
                                    {
                                    "title": "More Details",
                                    "url": externallink,
                                    "type": "web_url"
                                    }
                                ]
                            }
                        ]
                        }
                }
                dispatcher.utter_message(attachment=message)


#### combined coursel version 2

class ActionListAllEvents(Action):
    def name(self) -> Text:
        return "action_list_all_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_city = tracker.get_slot("event_city")
        event_artists = tracker.get_slot("event_artists")
        event_date = tracker.get_slot("event_date")
        event_category = tracker.get_slot("event_category")

        params = {
            "city": event_city or "",  
            "artists": event_artists or "",
            "startdate": event_date or "",
            "category": event_category or ""
        }

        event_api = EventAPI()
        events = event_api.get_events(params)

        if events:
            event_list = []
            coursel_elements = []

            for event in events:
                event_name = event.get("event_name", "N/A")
                event_location = event.get("street", "N/A")
                image_name = event.get("image_name", "N/A")
                externallink = event.get("externallink", "N/A")

                event_info = f"Event Name: {event_name}\nLocation: {event_location}\nImage: {image_name}\nLink: {externallink}\n"
                event_list.append(event_info)

                coursel_element = {
                    "title": event_name,
                    "subtitle": event_location,
                    "image_url": f"https://tic8m8.com/uploads/events/{image_name}",
                    "buttons": [
                        {
                            "title": "Contact Information",
                            "payload": f"Contact Information for {event_name}",
                            "type": "postback"
                        },
                        {
                            "title": "More Info",
                            "payload": f"More Information of {event_name}",
                            "type": "postback"
                        },
                        {
                            "title": "More Details",
                            "url": externallink,
                            "type": "web_url"
                        }
                    ]
                }
                coursel_elements.append(coursel_element)  # Append the carousel element

            response_message = "Here is the list of events:\n\n" + "\n".join(event_list)

            coursel_message = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": coursel_elements
                }
            }

            dispatcher.utter_message(response_message)
            dispatcher.utter_message(attachment=coursel_message)
        else:
            dispatcher.utter_message("There aren't any events based on your criteria. Why don't you check our events page? We have a whole catalog of events there! 😀")

        return []