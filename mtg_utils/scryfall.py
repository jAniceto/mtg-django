import requests


def get_card_by_name(name):
    """
    Searches a card by name on the Scryfall API. This function queries the Scryfall 'cards/named' API endpoint with an exact match search for the provided card name.
    Returns a Scryfall card object if a card is found, otherwise returns None

    Raises:
        requests.RequestException: An error from the `requests` library indicating a problem with the network or the
        fetch operation.
    """
    url = 'https://api.scryfall.com/cards/named'
    params = {'exact': name}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # The card exists, return card object
            return response.json()
    except requests.RequestException as e:
        print(f'An error occurred: {e}')
    return None
