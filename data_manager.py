import os
import requests
from dotenv import load_dotenv
#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

load_dotenv()


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.endpoint = os.environ.get("SHEET_ENDPOINT")
        self.token = os.environ.get("SHEET_API_TOKEN")
        self.auth = {
            "Authorization": f"Bearer {self.token}"
        }
        self.sheet_data = {}

    def get_excel_content(self):
        content = requests.get(url=self.endpoint, headers=self.auth)
        data = content.json()
        self.sheet_data = data['prices']
        return self.sheet_data

    def update_excel_content(self):
        for row in self.sheet_data:
            new_code_update = {
                'price': {
                    'iataCode' : row['iataCode']
                }
            }
            response = requests.put(url=f"{self.endpoint}/{row['id']}", headers=self.auth, json=new_code_update)
            print(response.text)