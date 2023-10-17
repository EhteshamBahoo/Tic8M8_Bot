import requests
from typing import (
    Any, Text, Dict, List,
    )
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from dateutil import parser
from datetime import datetime, timedelta
import re
import requests


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

###  empty all slots action
class ActionClearEventFilters(Action):
    def name(self) -> Text:
        return "action_clear_event_filters"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots_to_reset = ["event_city", "event_artists", "event_date", "event_category"]

        slot_resets = [SlotSet(slot, None) for slot in slots_to_reset]
        
        return slot_resets

### PAssing js
class ActionShowAlert(Action):
    def name(self):
        return "action_show_alert"

    def run(self, dispatcher, tracker, domain):
        # Send a message to trigger the JavaScript alert
        dispatcher.utter_message(text="show_alert")
        return []


###empty all slot action end

'''
Logic for sign up page if php passed the certain id then dont send
'''


""" List events Based on combined criteria using FORMS """


# Define a custom form to gather the required slots
class ActionEventSearch(Action):
    def name(self) -> Text:
        return "action_event_search_criteria"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        event_city = tracker.get_slot("event_city")
        event_category = tracker.get_slot("event_category")
        max_price = tracker.get_slot("max_price")

        params = {
            "city": event_city,
            "category": event_category,
        }

        original_max_price = max_price

        if max_price is not None and max_price.lower() == "free":
            params["isfree"] = True
        else:
            params["maxprice"] = max_price

        event_api = EventAPI()
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
                            "title": "More Information",
                            "payload": f"/ask_more_info{{\"event_name\":\"{event_name}\"}}",
                            "type": "postback"
                        },
                        {
                            "title": "More Details",
                            "url": externallink,
                            "type": "web_url"
                        }
                    ]
                }
                coursel_elements.append(coursel_element)

            coursel_message = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": coursel_elements
                }
            }
            
            dispatcher.utter_message(
                "Here is the list of events based on your criteria:"
            )
            dispatcher.utter_message(attachment=coursel_message)
        else:
            if "maxprice" in params:
                del params["maxprice"]
                events_without_max_price = event_api.get_events(params)
                if events_without_max_price:
                    coursel_elements = []

                    for event in events_without_max_price:
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
                                    "title": "More Information",
                                    "payload": f"/ask_more_info{{\"event_name\":\"{event_name}\"}}",
                                    "type": "postback"
                                },
                                {
                                    "title": "More Details",
                                    "url": externallink,
                                    "type": "web_url"
                                }
                            ]
                        }
                        coursel_elements.append(coursel_element)

                    coursel_message = {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": coursel_elements
                        }
                    }
                    
                    dispatcher.utter_message(
                        "There aren't any events based on your criteria. Here are the closest possible events for the chosen category:"
                    )
                    dispatcher.utter_message(attachment=coursel_message)
                else:
                    dispatcher.utter_message(
                        "There aren't any events based on your criteria. Why don't you check our events page? We have a whole catalog of events there! 😀"
                    )
            else:
                dispatcher.utter_message(
                    "There aren't any events based on your criteria. Why don't you check our events page? We have a whole catalog of events there! 😀"
                )

        return []







""" end """

## give istop events as buttons:
class ActionGiveIstopButtons(Action):
    def name(self) -> Text:
        return "action_give_istop_buttons"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Parameters for the EventAPI
        istop = True
        params = {
            "istop": istop
        }
        event_api = EventAPI()
        top_events = event_api.get_events(params)
        if top_events:
            top_events = top_events[:4]
            event_names = [event.get("event_name", "N/A") for event in top_events]
            buttons = [{"title": event_name, "payload": event_name} for event_name in event_names]
            dispatcher.utter_message(template="utter_ask_event_name")
            dispatcher.utter_button_message("Trending Events:", buttons)

        return []

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

            for event in events:
                event_name = event.get("event_name", "N/A")
                event_location = event.get("street", "N/A")

                event_info = f"Event Name: {event_name}\nStreet: {event_location}\n\n"
                event_list.append(event_info)

            response_message = "Here is the list of events:\n\n" + "\n".join(event_list)
            dispatcher.utter_message(response_message)
        else:
            dispatcher.utter_message("There aren't any events based on your criteria. Why don't you check our events page? We have a whole catalog of events there! 😀")

        return []


""" end """

""" Give ticket type information"""
class ActionGetTicketTypes(Action):
    def name(self) -> Text:
        return "action_get_ticket_types"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("event_name")
        ticket_type_name = tracker.latest_message.get("payload", {}).get("ticket_type", "N/A")

        if not event_name:
            dispatcher.utter_message("I couldn't find the event name.")
            return []

        eventdate_id = self.get_eventdate_id(event_name)

        if eventdate_id is not None:
            ticket_types = self.get_ticket_types(eventdate_id)
            if ticket_types:
                response_message = "Here are the ticket types:\n\n"
                buttons = []  # Create an empty list for buttons

                for ticket_type in ticket_types:
                    name = ticket_type.get("name", "N/A")
                    price = ticket_type.get("price", "N/A")
                    response_message += f"Name: {name}  \n||  Price: {price}        \n\n"

                    # Append each ticket type as a button with the payload
                    buttons.append({"title": name, "payload": f"/give_ticket_type{{\"ticket_type\":\"{name}\"}}"})

                dispatcher.utter_message(response_message)

                # Send all the buttons at once
                dispatcher.utter_button_message("Please select a ticket type:", buttons)

                # Set the selected ticket type to the slot
                return [SlotSet("ticket_type", ticket_type_name)]
            else:
                dispatcher.utter_message("No event types found for the given event.")
        else:
            dispatcher.utter_message(f"No event found with the name '{event_name}'.")

        return []

    def get_eventdate_id(self, event_name: Text) -> int:
        url = "https://dev.tic8m8.com/api/getevents"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }
        params = {"name": event_name}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                eventdate_id = data[0].get("eventdate_id")
                return eventdate_id
        except requests.exceptions.RequestException:
            pass
        return None

    def get_ticket_types(self, eventdate_id: int) -> List[Dict[Text, Any]]:
        url = "https://dev.tic8m8.com/api/geteventtypes"
        params = {"eventdate_id": eventdate_id}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
        except requests.exceptions.RequestException:
            pass
        return []

"""   """


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
                                "title": "More Information",
                                "payload": f"/ask_more_info{{\"event_name\":\"{event_name}\"}}",
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

class ActionListRecommendedIstopEvents(Action):
    def name(self) -> Text:
        return "action_list_top_events"

    def run(self, dispatcher: "CollectingDispatcher", 
            tracker: Tracker, domain: List[Dict[Text, Any]]
            ) -> List[Dict[Text, Any]]:


            event_api = EventAPI()
            params = {"istop": True}
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
                                    "title": "More Information",
                                    "payload": f"/ask_more_info{{\"event_name\":\"{event_name}\"}}",
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

                        # event_info = f"Event: {event_name} at address: {event_location}"
                        # event_list.append(event_info)

                    response_message = "Here are some events that I am recommending to you Have a look and let me know\n\n" + "\n".join(event_list)
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
                   
            return []


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
                                    "title": "More Information",
                                    "payload": f"/ask_more_info{{\"event_name\":\"{event_name}\"}}",
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



""" -- COursel Code end """

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
            dispatcher.utter_message(template="utter_give_moreinfo", event_name=event_name, event_link=external_link)
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


class ActionGetTicketDetails(Action):
    def name(self) -> Text:
        return "action_get_ticket_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("ticket_type")
        ticket_type_name = tracker.latest_message.get("payload", {}).get("ticket_type", "N/A")

        if not event_name:
            dispatcher.utter_message("I couldn't find the event name.")
            return []

        eventdate_id = self.get_eventdate_id(event_name)

        if eventdate_id is not None:
            ticket_type = self.get_ticket_type(eventdate_id, ticket_type_name)
            if ticket_type:
                name = ticket_type.get("name", "N/A")
                price = ticket_type.get("price", "N/A")
                description = ticket_type.get("description", "N/A")

                response_message = f"Ticket Name: {name}\nDescription: {description}"
                dispatcher.utter_message(response_message)

                # Set the selected ticket type to the slot
                return [SlotSet("ticket_type", name)]
            else:
                dispatcher.utter_message(f"No information found for the ticket type '{ticket_type_name}'.")
        else:
            dispatcher.utter_message(f"No event found with the name '{event_name}'.")

        return []

    def get_eventdate_id(self, event_name: Text) -> int:
        url = "https://dev.tic8m8.com/api/getevents"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }
        params = {"name": event_name}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                eventdate_id = data[0].get("eventdate_id")
                return eventdate_id
        except requests.exceptions.RequestException:
            pass
        return None

    def get_ticket_type(self, eventdate_id: int, ticket_type_name: Text) -> Dict[Text, Any]:
        url = "https://dev.tic8m8.com/api/geteventtypes"
        params = {"eventdate_id": eventdate_id}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                for ticket_type in data:
                    if ticket_type.get("name") == ticket_type_name:
                        return ticket_type
        except requests.exceptions.RequestException:
            pass
        return {}
####----------------------------------------------------------------

