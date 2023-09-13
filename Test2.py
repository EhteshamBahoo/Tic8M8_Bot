import requests

def get_event_address(event_name):
    api_url = f"https://dev.tic8m8.com/api/getevents?name={event_name}"


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if 'address' in data:
                print("Event Address:", data['address'])
            else:
                print("Address not found in the API response.")
        else:
            print("Failed to retrieve data from the API. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the API request:", str(e))

# Example usage:
event_name = "Disney On Ice: 100 Years of Wonder Abu Dhabi 2023"
get_event_address(event_name)
