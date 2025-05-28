import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from pprint import pprint
from notification_manager import NotificationManager

flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_excel_content()
notification_manager = NotificationManager()

# Change to your origin city
ORIGIN_CITY_IATA = "MCO"

# Get IataCode for each destination
# for row in sheet_data:
#     if row['iataCode']== '':
#         row["iataCode"] = flight_search.get_iataCode(row["city"])
#         time.sleep(2)
# pprint(sheet_data)
#
data_manager.sheet_data = sheet_data
# data_manager.update_excel_content()

tomorrow = datetime.now() +timedelta(days=1)
six_month = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.get_flight_info(
        original_code=ORIGIN_CITY_IATA,
        destination_code=destination['iataCode'],
        departure_date=tomorrow.strftime("%Y-%m-%d"),
        return_date=six_month.strftime("%Y-%m-%d"),
        currency="USD", #Change your currency if needed
        adults=1,
        nonstop="true",
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}:{cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination['lowestPrice']:
        print(f"Lower price found to {destination['city']}!")
        notification_manager.send_message(
            message_body=f"Low price alert! Only ${cheapest_flight.price} to fly "
                        f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport},"
                        f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )