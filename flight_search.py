import os
import requests

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ.get("AMADEUS_API_KEY")
        self._api_secret = os.environ.get("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):
        """get new token from amadeus each run in case the previous one expired"""
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()['access_token']

    def get_iataCode (self, city_name):
        """get IataCode for the destination cities"""
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}")
            return
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}")
            return
        return code

    def get_flight_info(self, original_code, destination_code, departure_date, return_date, currency, adults, nonstop):
        """get all flight info. It's a large chunk of data."""
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "originLocationCode": original_code,
            "destinationLocationCode": destination_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": adults,
            "nonStop": nonstop,
            "currencyCode": currency,
            "max": "10"
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)

        if response.status_code != 200:
            print(response.status_code)
            print('There is a problem with flight searching.')
            print(response.text)
            return None

        return response.json()