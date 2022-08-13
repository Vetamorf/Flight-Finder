import requests
from flight_search import get_iata_code


GOOGLE_SHEETS_URL_PRICES = 'https://api.sheety.co/b9a158d10c51bfedf429994dde934a01/pythonFlightDeals2/prices'


class DataManager:
    # This class is responsible for talking to the Google Sheet Prices.
    def __init__(self):
        price_response = requests.get(url=GOOGLE_SHEETS_URL_PRICES)
        price_response.raise_for_status()
        self.price_data = price_response.json()['prices']

    def update_iata_codes(self):
        for city_number in range(len(self.price_data)):
            city_name = self.price_data[city_number]['city']
            iata_code = get_iata_code(city_name)
            self.price_data[city_number]['iataCode'] = iata_code

            body = {
                "price": {
                    'iataCode': iata_code
                }
            }
            requests.put(url=f"{GOOGLE_SHEETS_URL_PRICES}/{city_number + 2}", json=body)
