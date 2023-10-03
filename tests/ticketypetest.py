import requests

# Function to get eventdate_id for a given event_name
def get_eventdate_id(event_name):
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
            if eventdate_id is not None:
                return eventdate_id
        print(f"No eventdate_id found for '{event_name}'.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching eventdate_id: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to get event types for a given eventdate_id
def get_event_types(eventdate_id):
    url = f"https://dev.tic8m8.com/api/geteventtypes?eventdate_id={eventdate_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if there is ticket data
        if isinstance(data, list) and len(data) > 0:
            for ticket in data:
                name = ticket.get("name")
                price = ticket.get("price")
                print(f"Name: {name}, Price: {price}")
        else:
            print("No event types found for the given eventdate_id.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching event types: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    event_name = input("Enter the event name: ")
    eventdate_id = get_eventdate_id(event_name)

    if eventdate_id is not None:
        print(f"Eventdate ID for '{event_name}': {eventdate_id}")
        print("Event Types:")
        get_event_types(eventdate_id)
