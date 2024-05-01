import requests

def website_opens_successfully(url: str):
    try:
        response = requests.get(url, timeout=5)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return False
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return False
    else:
        print('Website is up and running.')
        return True

# Usage
website_is_live = website_opens_successfully('https://www.cobycatsol.com/')
print(website_is_live)
