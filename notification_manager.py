import os
from twilio.rest import Client

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_TOKEN'])

    def send_message(self, message_body):
        """sending notification through Twilio to reception's Whatsapp"""
        message =self.client.messages.create(
            from_=f"whatsapp:{os.environ['TWILIO_NUMBER']}",
            body=message_body,
            to=f"whatsapp:{os.environ['MY_NUMBER']}"
        )
        print(message.sid)