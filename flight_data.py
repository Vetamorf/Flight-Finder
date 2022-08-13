class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, from_airport, to_airport, from_city, to_city, price, link: str, departure_date, return_date, currency):
        self.price = price
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.from_city = from_city
        self.to_city = to_city
        self.link = link
        self.departure_date = departure_date
        self.return_date = return_date
        self.currency = currency
        self.transfer_cities_to = []
        self.transfer_cities_back = []
        self.transfer_cities = []
