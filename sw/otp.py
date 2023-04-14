from django.conf import settings
from twilio.rest import Client


"""
MessageHandler class that takes two arguments: OTP and phone_number. 
Phone_number is the phone number to which we want to send an OTP.
We have two functions in this class: one that is responsible for sending SMS and the other for sending WhatsApp messages.
We initialize the Client in both functions first, and then we send messages using Twilio functions.
Note that in the WhatsApp function, we will use a sandbox phone number instead of the number given to us by Twilio.
"""

class MessageHandler:
    phone_number = None
    otp = None
    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_via_message(self):     
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=f'Your OTP is : {self.otp}', from_ = f'{settings.TWILIO_PHONE_NUMBER}', to = f'{settings.COUNTRY_CODE}{self.phone_number}')
        
    # def send_otp_via_whatsapp(self):     
    #     client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    #     message = client.messages.create(body=f'Your OTP is : {self.otp}', from_ =f'{settings.TWILIO_WHATSAPP_NUMBER}', to = f'whatsapp:{settings.COUNTRY_CODE}{self.phone_number}')