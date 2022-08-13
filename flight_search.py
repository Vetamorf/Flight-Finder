import requests
from flight_data import FlightData
import datetime as dt
from pprint import pprint

# This file is responsible for talking to the Flight Search API.

TEQUILA_LOCATION_ENDPOINT = 'https://tequila-api.kiwi.com/locations/query'
TEQUILA_FLIGHTS_ENDPOINT = 'https://tequila-api.kiwi.com/v2/search'
TEQUILA_API_KEY = "VDUUcOREP9qWyUf7aRfGahWVIYgkFjDQ"

HEADER = {
    'apikey': TEQUILA_API_KEY
}


def get_iata_code(city_name: str) -> str:
    parameters = {
        'term': city_name,
        'location_types': 'airport'
    }
    location_response = requests.get(url=TEQUILA_LOCATION_ENDPOINT, params=parameters, headers=HEADER)
    location_response.raise_for_status()
    city_code = location_response.json()['locations'][0]['city']['code']

    return city_code


def get_tomorrow_date():
    today = dt.datetime.now()
    tomorrow = today + dt.timedelta(days=1)
    tomorrow = tomorrow.strftime('%d/%m/%Y')
    return tomorrow


def get_six_month_later_date():
    today = dt.datetime.now()
    six_months_later = today + dt.timedelta(days=183)
    six_months_later = six_months_later.strftime('%d/%m/%Y')
    return six_months_later


def find_flights(city_code_from, city_code_to, city_to, currency):
    params = {
        'fly_from': city_code_from,
        'fly_to': city_code_to,
        'dateFrom': get_tomorrow_date(),
        'dateTo': get_six_month_later_date(),
        'nights_in_dst_from': 1,
        'nights_in_dst_to': 16,
        'flight_type': 'round',
        'one_for_city': 1,
        "max_stopovers": 0,
        "curr": currency
    }

    response = requests.get(url=TEQUILA_FLIGHTS_ENDPOINT, params=params, headers=HEADER)
    response.raise_for_status()

    transfer_cities_to = []
    transfer_cities_back = []

    try:
        flight_response = response.json()['data'][0]
        flight_routs = flight_response['route']
        num_of_stopovers = 0
    except IndexError:
        # If no direct flight has been found check flights with up to 2 stopover (1 stopover for each direction)
        params['max_stopovers'] = 2

        response = requests.get(url=TEQUILA_FLIGHTS_ENDPOINT, params=params, headers=HEADER)
        response.raise_for_status()

        try:
            flight_response = response.json()['data'][0]
            flight_routs = flight_response['route']
            num_of_stopovers = len(flight_routs) - 2
        except IndexError:
            print(f'No flights to {city_to} has been found.')
            return None
        else:
            is_flying_to_dst = True

            for flights in flight_routs:
                if flights['cityCodeTo'] == city_code_to:
                    # Now we are flying back
                    is_flying_to_dst = False
                    continue
                elif flights['cityCodeTo'] == city_code_from:
                    continue

                if is_flying_to_dst:
                    transfer_cities_to.append(flights['cityTo'])
                else:
                    transfer_cities_back.append(flights['cityTo'])

    to_stop_overs = len(transfer_cities_to)

    departure_date = flight_routs[0]['local_departure'].split('T')[0]
    return_date = flight_routs[to_stop_overs + 1]['local_departure'].split('T')[0]

    flight_data = FlightData(from_airport=flight_response['cityCodeFrom'],
                             to_airport=flight_response['cityCodeTo'],
                             from_city=flight_response['cityFrom'],
                             to_city=flight_response['cityTo'],
                             price=flight_response['conversion'][currency],
                             link=flight_response['deep_link'],
                             departure_date=departure_date,
                             return_date=return_date,
                             currency=currency)

    if num_of_stopovers > 0:
        flight_data.transfer_cities_to = transfer_cities_to
        flight_data.transfer_cities_back = transfer_cities_back
        flight_data.transfer_cities = transfer_cities_to + transfer_cities_back

    print(f'{flight_data.to_city}: {flight_data.price} {currency}')
    return flight_data
