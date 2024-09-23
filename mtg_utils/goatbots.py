import json
import requests
import zipfile
from pathlib import Path
from io import BytesIO


URL_PRICES = 'https://www.goatbots.com/download/price-history.zip'
URL_CARD_DEFINITIONS = 'https://www.goatbots.com/download/card-definitions.zip'


def download_data(url: str, save_to: Path):
    """
    Download price data from GoatBoats. It fetches the data, unzips in memory, converts to JSON, and saves to disk.
    :param url: ZIP file to download.
    :param save_to: Output file folder.
    """
    # Fetch data
    response = requests.get(url)
    response.raise_for_status()

    # Unzip and read into JSON
    with zipfile.ZipFile(BytesIO(response.content)) as thezip:
        # Iterate over each file in the ZIP
        for zip_info in thezip.infolist():
            # Open the file inside the ZIP as another BytesIO object (in-memory file)
            with thezip.open(zip_info) as file:
                # Read file
                contents = file.read().decode('utf-8')
                json_data = json.loads(contents)

    # Save JSON data to disk
    local_filename = url.split('/')[-1].replace('.zip', '')
    out_file = save_to / f'{local_filename}.json'
    with open(out_file, 'w') as f:
        json.dump(json_data, f)

    print(f'GoatBots data saved to {out_file}.')


def get_prices(card_name: str, prices_dir: Path, exclude_foils=False):
    """
    Get prices of a card with a given name.
    :param card_name: Name of card to get prices.
    :param prices_dir: Path to directory with GoatBots prices and card definitions.
    :param exclude_foils: Set True to exclude foils from search.
    :return: List of price objects in the format: {'name': 'Rancor', 'set': '2X2', 'foil': False, 'price': 0.1}
    """
    # Data file locations
    card_definitions_file = prices_dir / 'card-definitions.json'
    prices_file = prices_dir / 'price-history.json'

    # Load card definitions file
    with open(card_definitions_file, 'r') as f:
        card_defs = json.load(f)

    # Find all versions of desired card
    card_objects = {
        k: v for k, v in card_defs.items() if isinstance(v, dict) and card_name in v.values()
    }

    # Exclude foils?
    if exclude_foils:
        card_objects = {
            k: v for k, v in card_objects.items() if isinstance(v, dict) and v['foil'] == 0
        }

    # Load card prices file
    with open(prices_file, 'r') as f:
        goatbot_prices = json.load(f)

    # Return a prices dictionary
    prices = []
    for mtgo_id, values in card_objects.items():
        prices.append(
            {
                'name': card_name,
                'set': values['cardset'],
                'foil': False if values['foil'] == 0 else True,
                'price': goatbot_prices[mtgo_id],
            }
        )
    return prices


def get_best_price(price_obj_list):
    """
    Get the best price object
    :param price_obj_list: List of price objects. The output of get_prices().
    :return: The object with the best price.
    """
    sorted_price_objs = sorted(price_obj_list, key=lambda x: (x['price']))
    return sorted_price_objs[0]
