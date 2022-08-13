import smtplib
from flight_data import FlightData
from user_ui_manager import emails


def generate_message(flight_data: FlightData):
    stop_overs = len(flight_data.transfer_cities)
    transfer_cities_without_repeat = list(set(flight_data.transfer_cities))

    transfer_cities = ' and '.join(transfer_cities_without_repeat)

    if stop_overs == 1:
        plural = ''
    elif stop_overs > 1:
        plural = 's'

    body_msg = f'Subject: Low-Cost Flight: ' \
               f'{flight_data.from_city.upper()} - {flight_data.to_city.upper()} \n\n' \
               f'Low price alert! \n\n' \
               f'Only {flight_data.price} {flight_data.currency} for a round trip: \n' \
               f'         {flight_data.from_city}-{flight_data.from_airport}   -   ' \
               f'{flight_data.to_city}-{flight_data.to_airport} \n' \
               f'         from {flight_data.departure_date} to {flight_data.return_date}\n\n'

    text_link = flight_data.link.replace('affilid=vetamorfflightsearch&', '')
    link = f'Link: {text_link}'

    if stop_overs > 0:
        stop_overs_info = f'Flight has {stop_overs} stop over{plural}, via {transfer_cities}.\n\n'
    else:
        stop_overs_info = ''

    message = body_msg + stop_overs_info + link
    return message


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.my_gmail = "test.fateeva.liza@gmail.com"
        self.my_password = 'ahakgpbgchmdacaf'

    def send_notification_letter(self, flight_data: FlightData):
        msg = generate_message(flight_data)

        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=self.my_gmail, password=self.my_password)
            connection.sendmail(from_addr=self.my_gmail,
                                to_addrs=emails,
                                msg=msg.encode('utf-8'))
