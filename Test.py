import requests
from typing import (
    Any, Text, Dict, List
    )
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import datetime

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



## Range  code

class ActionListEventsByPriceRange(Action):
    def name(self) -> Text:
        return "action_list_events_by_price_range"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        min_price = tracker.get_slot("min_price")  # Extract the minimum price from the slot
        max_price = tracker.get_slot("max_price")  # Extract the maximum price from the slot

        if min_price is not None and max_price is not None:
            event_api = EventAPI()  # Create an instance of your EventAPI class
            params = {"minprice": min_price, "maxprice": max_price}
            events = event_api.get_events(params)

            if events:
                event_list = []

                for event in events:
                    event_name = event.get("event_name", "N/A")
                    event_location = event.get("street", "N/A")

                    event_info = f"Event: {event_name}, Location: {event_location}"
                    event_list.append(event_info)

                response_message = "Here are the events within the specified price range:\n\n" + "\n".join(event_list)
                dispatcher.utter_message(response_message)
            else:
                dispatcher.utter_message("No events found within the specified price range.")
        else:
            dispatcher.utter_message("Please provide both a minimum and maximum price to search for events.")

        return []



#### search by DATE


### code for relative date


"""  Code for List by Date  """

class ActionListEventsByMinPrice(Action):
    def name(self) -> Text:
        return "action_list_events_by_date"

    def run(self, dispatcher: "CollectingDispatcher", 
            tracker: Tracker, domain: List[Dict[Text, Any]]
            ) -> List[Dict[Text, Any]]:
            min_price = tracker.get_slot("event_date")  # Extract the minimum price from the slot

            if min_price is not None:
                event_api = EventAPI()
                params = {"startdate": min_price}
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
        

class ActionListEventsByMinPrice(Action):
    def name(self) -> Text:
        return "action_list_events_by_date"

    def run(self, dispatcher: "CollectingDispatcher", 
            tracker: Tracker, domain: List[Dict[Text, Any]]
            ) -> List[Dict[Text, Any]]:
            event_date = tracker.get_slot("event_date")  # Extract the minimum price from the slot

            if event_date is not None:
                event_api = EventAPI()
                params = {"enddate": event_date}
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


### REPLACE EVENT DATE WITH TWO NEW SLOTS


class ActionListEventsByDate(Action):
    def name(self) -> Text:
        return "action_list_events_by_date"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Extract start_date and end_date from slots
        start_date = tracker.get_slot("start_date")
        end_date = tracker.get_slot("end_date")

        # Check if both start_date and end_date are available
        if start_date and end_date:
            # Parse the date strings to datetime objects (you may need to adjust the date format)
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")

                # Now, you can use start_date and end_date to filter events
                event_api = EventAPI()  # Create an instance of your EventAPI class
                params = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
                events = event_api.get_events(params)

                if events:
                    # Create a list of event details (customize as needed)
                    event_list = []
                    for event in events:
                        event_name = event.get("event_name", "N/A")
                        event_location = event.get("street", "N/A")
                        event_date = event.get("event_date", "N/A")
                        # Add more event details as needed
                        event_info = f"Event: {event_name}\nLocation: {event_location}\nDate: {event_date}\n\n"
                        event_list.append(event_info)

                    response_message = "Here are the events within your specified date range:\n\n" + "\n".join(event_list)
                    dispatcher.utter_message(response_message)
                else:
                    dispatcher.utter_message("No events found within the specified date range.")
            except ValueError:
                dispatcher.utter_message("Invalid date format. Please provide dates in YYYY-MM-DD format.")
        else:
            dispatcher.utter_message("Please provide both start and end dates for event filtering.")

        return []


"""Form Actions"""

class ActionListTicketTypes(Action):
    def name(self) -> str:
        return "action_list_ticket_types"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        event_name = tracker.get_slot("event_name")
        
        if not event_name:
            dispatcher.utter_message("Please provide the event name.")
            return []
        
        eventdate_id = self.get_eventdate_id(event_name)
        
        if not eventdate_id:
            dispatcher.utter_message("Event not found or event date not available.")
            return []
        ticket_types = self.get_ticket_types(eventdate_id)

        if ticket_types:
            ticket_type_list = []

            for ticket_type in ticket_types:
                ticket_name = ticket_type.get("ticket_name", "N/A")
                ticket_price = ticket_type.get("ticket_price", "N/A")

                ticket_info = f"Ticket Type: {ticket_name}, Price: {ticket_price} AED"
                ticket_type_list.append(ticket_info)

            response_message = "Here are the available ticket types:\n\n" + "\n".join(ticket_type_list)
            dispatcher.utter_message(response_message)
        else:
            dispatcher.utter_message("No ticket types found for the specified event.")

        return []

    def get_eventdate_id(self, event_name: str) -> str:
        # Implement the logic to fetch eventdate_id based on the event_name from your API
        # Example: You can make an API request to retrieve the eventdate_id
        # Replace the return statement with your actual logic
        eventdate_id = "12345"  # Replace with the actual eventdate_id
        return eventdate_id

    def get_ticket_types(self, eventdate_id: str) -> List[Dict[Text, Any]]:
        # Implement the logic to fetch ticket types using eventdate_id from your API
        # Example: You can make an API request to retrieve ticket types
        # Replace the return statement with your actual logic
        ticket_types = [
            {"ticket_name": "General Admission", "ticket_price": 50},
            {"ticket_name": "VIP", "ticket_price": 100},
            {"ticket_name": "Student", "ticket_price": 25},
        ]  # Replace with the actual ticket types from your API
        return ticket_types