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

    def get_login(self, params: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        return  self.base_url 

# ### -remove this or comment

# class MyCustomAction(Action):
#     def name(self):
#         return "action_send_html_response"

#     def run(self, dispatcher, tracker, domain):
#         html_message = "<b>This is a bold message</b> <a href='https://tic8m8.com'>Click here</a>"
        
#         dispatcher.utter_message(text=html_message, html=True)

#         return []
# ### -end

# ### DATE PICKER CODE

# class ActionAskDate(Action):
#     def name(self) -> Text:
#         return "action_ask_date"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message("Please select a date using the date picker.")
#         return []

# class ActionProcessDate(Action):
#     def name(self) -> Text:
#         return "action_process_date"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         selected_date = tracker.latest_message.get('text')
#         dispatcher.utter_message(f"You have selected the date: {selected_date}")
#         return []

# ###


###  empty all slots action
class ActionClearEventFilters(Action):
    def name(self) -> Text:
        return "action_clear_event_filters"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots_to_reset = ["event_city", "event_artists", "event_date", "event_category"]

        slot_resets = [SlotSet(slot, None) for slot in slots_to_reset]
        
        return slot_resets

###empty all slot action end

'''
Logic for sign up page if php passed the certain id then dont send
'''

#### combined coursel version 2
#### List events city and category

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
                coursel_elements.append(coursel_element) # putting a single element into a collection of elements

            response_message = "Here is the list of events \n\n" + "\n".join(event_list)
                
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
                dispatcher.utter_message("There arent any events based on your criteria why dont you check our events page we have a whole catalog of events there! 😀") 

        return []

# Event List with MAX Price
class ActionListEventsByMaxPrice(Action):
    def name(self) -> Text:
        return "action_list_events_by_maxprice"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        max_price = tracker.get_slot("max_price")  # Extract the maximum price from the slot

        if max_price is not None:
            event_api = EventAPI()  # Create an instance of your EventAPI class
            params = {"maxprice": max_price}
            events = event_api.get_events(params)

            if events:
                coursel_elements = []

                for event in events:
                    event_name = event.get("event_name", "N/A")
                    event_location = event.get("street", "N/A")
                    image_name = event.get("image_name", "N/A")
                    externallink = event.get("externallink", "N/A")

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
                    coursel_elements.append(coursel_element)  # putting a single element into a collection of elements

                coursel_message = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": coursel_elements
                    }
                }
                dispatcher.utter_message(attachment=coursel_message)
            else:
                dispatcher.utter_message("No events found within the specified price range.")
        else:
            dispatcher.utter_message("I couldn't find a maximum price. Please provide a valid maximum price.")

        return []

## adding coode for min price value search


class ActionListEventsByMinPrice(Action):
    def name(self) -> Text:
        return "action_list_events_by_minprice"

    def run(self, dispatcher: "CollectingDispatcher", 
            tracker: Tracker, domain: List[Dict[Text, Any]]
            ) -> List[Dict[Text, Any]]:
            min_price = tracker.get_slot("min_price")  # Extract the minimum price from the slot

            if min_price is not None:
                event_api = EventAPI()
                params = {"minprice": min_price}
                events = event_api.get_events(params)

                if events:
                    event_list = []
                    coursel_elements = []

                    for event in events:
                        event_name = event.get("event_name", "N/A")
                        event_location = event.get("street", "N/A")
                        image_name = event.get("image_name", "N/A")
                        externallink = event.get("externallink", "N/A")

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
                        coursel_elements.append(coursel_element)  # Append to carousel elements

                        event_info = f"Event: {event_name} at address: {event_location}"
                        event_list.append(event_info)

                    response_message = "Here are the events that cost less than your specified price:\n\n" + "\n".join(event_list)
                    dispatcher.utter_message(response_message)

                    coursel_message = {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": coursel_elements
                        }
                    }
                    dispatcher.utter_message(attachment=coursel_message)
                else:
                    dispatcher.utter_message("No events found within the specified price range.")
            else:
                dispatcher.utter_message("I couldn't find a maximum price. Please provide a valid maximum price.")
                   
            return []
        
## price range code
## NO RANGE ADD DATE & then checkout

class ActionListEventsByPriceRange(Action):
    def name(self) -> Text:
        return "action_list_events_by_price_range"

    def run(self, dispatcher: "CollectingDispatcher", 
            tracker: Tracker, domain: List[Dict[Text, Any]]
            ) -> List[Dict[Text, Any]]:
            min_price = tracker.get_slot("min_price")  # Extract the minimum price from the slot
            max_price = tracker.get_slot("max_price")  # Extract the maximum price from the slot

            if min_price is not None and max_price is not None:
                event_api = EventAPI()
                params = {"minprice": min_price, "maxprice": max_price}
                events = event_api.get_events(params)

                if events:
                    event_list = []

                    for event in events:
                        event_name = event.get("event_name", "N/A")
                        event_location = event.get("street", "N/A")

                        event_info = f"Event: {event_name} at address: {event_location}"
                        event_list.append(event_info)

                    response_message = "Here are the events within your specified price range:\n\n" + "\n".join(event_list)
                    dispatcher.utter_message(response_message)
                else:
                    dispatcher.utter_message("No events found within the specified price range.")
            else:
                dispatcher.utter_message("Please provide both a valid minimum and maximum price.")

            return []

# class ActionListEventsByPriceRange(Action):
#     def name(self) -> Text:
#         return "action_list_events_by_price_range"

#     def run(self, dispatcher: "CollectingDispatcher", 
#             tracker: Tracker, domain: List[Dict[Text, Any]]
#             ) -> List[Dict[Text, Any]]:
#             min_price = tracker.get_slot("min_price")  # Extract the minimum price from the slot
#             max_price = tracker.get_slot("max_price")  # Extract the maximum price from the slot

#             if min_price is not None and max_price is not None:
#                 event_api = EventAPI()
#                 params = {"minprice": min_price, "maxprice": max_price}
#                 events = event_api.get_events(params)

#                 if events:
#                     event_list = []
#                     coursel_elements = []

#                     for event in events:
#                         event_name = event.get("event_name", "N/A")
#                         event_location = event.get("street", "N/A")
#                         image_name = event.get("image_name", "N/A")
#                         externallink = event.get("externallink", "N/A")

#                         coursel_element = {
#                             "title": event_name,
#                             "subtitle": event_location,
#                             "image_url": f"https://tic8m8.com/uploads/events/{image_name}",
#                             "buttons": [
#                                 {
#                                     "title": "Contact Information",
#                                     "payload": f"Contact Information for {event_name}",
#                                     "type": "postback"
#                                 },
#                                 {
#                                     "title": "More Info",
#                                     "payload": f"More Information of {event_name}",
#                                     "type": "postback"
#                                 },
#                                 {
#                                     "title": "More Details",
#                                     "url": externallink,
#                                     "type": "web_url"
#                                 }
#                             ]
#                         }
#                         coursel_elements.append(coursel_element)  # Append to carousel elements

#                         event_info = f"Event: {event_name} at address: {event_location}"
#                         event_list.append(event_info)

#                     response_message = "Here are the events within your specified price range:\n\n" + "\n".join(event_list)
#                     dispatcher.utter_message(response_message)

#                     coursel_message = {
#                         "type": "template",
#                         "payload": {
#                             "template_type": "generic",
#                             "elements": coursel_elements
#                         }
#                     }
#                     dispatcher.utter_message(attachment=coursel_message)
#                 else:
#                     dispatcher.utter_message("No events found within the specified price range.")
#             else:
#                 dispatcher.utter_message("Please provide both a valid minimum and maximum price.")

#             return []

### -- COursel Code end

# Get Event Information

class ActionGetEventLocation(Action):
    def name(self) -> Text:
        return "action_get_event_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("event_name")

        event_api = EventAPI()
        params = {"name": event_name}
        events = event_api.get_events(params)

        if events:
            event = events[0]
            e_address = event.get("street", "Not applicatble")
            dispatcher.utter_message(template="utter_location_by_name", event_name=event_name, event_location=e_address)
            return [SlotSet("event_location", e_address)]
        else:
            dispatcher.utter_message("I couldn't find information for that event.")
            return [SlotSet("event_location", None)]



class ActionGetEventDate(Action):
    def name(self) -> Text:
        return "action_get_event_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("event_name")

        event_api = EventAPI()
        params = {"name": event_name}
        events = event_api.get_events(params)

        if events: 
            event = events[0]
            start_date = event.get("startdate", "N/A")
            dispatcher.utter_message(template="utter_date_by_name", event_name=event_name, event_date=start_date)
            return [SlotSet("event_date", start_date)]
        else:
            dispatcher.utter_message("I couldn't find information for that event.")
            return [SlotSet("event_date", None)]

class ActionGetEventLink(Action):
    def name(self) -> Text:
        return "action_get_event_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("event_name")

        event_api = EventAPI()
        params = {"name": event_name}
        events = event_api.get_events(params)

        if events:
            event = events[0]
            external_link = event.get("externallink", "N/A")
            dispatcher.utter_message(template="utter_give_list_all", event_name=event_name, event_link=external_link)
            return [SlotSet("event_link", external_link)]
        else:
            dispatcher.utter_message("I couldn't find information for that event.")
            return [SlotSet("event_link", None)]


class ActionGetEventContactInfo(Action):
    def name(self) -> Text:
        return "action_get_event_contact_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("event_name")

        event_api = EventAPI()
        params = {"name": event_name}
        events = event_api.get_events(params)

        if events:
            event = events[0]
            email = event.get("email", "N/A")
            phonenumber = event.get("phonenumber", "N/A")
            dispatcher.utter_message(template="utter_give_contactinfo", event_name=event_name, event_email=email, event_phonenumber=phonenumber)
            return [SlotSet("event_email", email), SlotSet("event_phonenumber", phonenumber)]
        else:
            dispatcher.utter_message("I couldn't find information for that event.")
            return [SlotSet("event_email", None), SlotSet("event_phonenumber", None)]
