from data_manager import DataManager
from flight_search import find_flights
from notification_manager import NotificationManager

CITY_CODE_FROM = 'BEG'
CURRENCY = 'EUR'


data_manager = DataManager()
notification_manager = NotificationManager()

# data_manager.update_iata_codes()

for destination in data_manager.price_data:
    city_code_to = destination['iataCode']
    city_to = destination['city']

    if city_code_to != CITY_CODE_FROM:
        lowest_price = destination['lowestPrice']
        flight_data = find_flights(CITY_CODE_FROM, city_code_to, city_to, CURRENCY)

        if flight_data is not None and flight_data.price <= lowest_price:
            notification_manager.send_notification_letter(flight_data)
