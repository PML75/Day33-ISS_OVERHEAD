from datetime import datetime
import requests
import smtplib
from twilio.rest import Client
import time

TOLL_PHONE = "blank"
PHONE_NUMBER = "blank"

account_sid = 'blank'
auth_token = 'blank'

MY_LAT = 33.74610154205828
MY_LONG = -117.96153702296485


def send_sms():
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=TOLL_PHONE,
        body='ISS_OVERHEAD',
        to=PHONE_NUMBER
    )


def iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True;


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    if iss_overhead() and is_night():
        send_sms()
    time.sleep(60)



