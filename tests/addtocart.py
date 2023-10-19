import requests

def get_ticket_id(event_name, ticket_type):

    eventdate_id = get_eventdate_id(event_name)
    if eventdate_id is not None:
        event_types = get_event_types(eventdate_id)
        for event_type in event_types:
            if event_type.get("name") == ticket_type:
                return event_type.get("id")
    return None

def get_user_id(user_id):

    user_id = get_user_id(user_id)
    if user_id is not None:
        
        return[]

def get_eventdate_id(event_name):

    url = "https://dev.tic8m8.com/api/getevents"
    params = {"name": event_name}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("eventdate_id")
    except requests.exceptions.RequestException:
        pass
    return None

def get_event_types(eventdate_id):

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

def add_tickets_to_cart(user_id, event_name, ticket_type, ticket_quantity):
    cart_api_url = ""
    ticket_id = get_ticket_id(event_name, ticket_type)
    if ticket_id is not None:
        cart_payload = {
            "user_id": user_id,
            "event_name": event_name,
            "ticket_id": ticket_id,
            "quantity": ticket_quantity,
        }
        try:
            response = requests.post(cart_api_url, json=cart_payload)
            if response.status_code == 200:
                print(f"Successfully added {ticket_quantity} {ticket_type} ticket(s) to your cart.")
            else:
                print("There was an issue adding tickets to your cart. Please try again later.")
        except requests.exceptions.RequestException as e:
            print("There was an error while processing your request. Please try again later.")

if __name__ == "__main__":
    user_id = "12345"
    event_name = input("Enter the event name: ")
    ticket_type = input("Enter the ticket type: ")
    ticket_quantity = int(input("Enter the ticket quantity: "))

    add_tickets_to_cart(user_id, event_name, ticket_type, ticket_quantity)
