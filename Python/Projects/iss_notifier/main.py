import requests
import time
import smtplib
from datetime import datetime


MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude
LOC_BUFFER = 5  # Buffer distance in degrees
EMAIL= ""
EMAIL_PASSWORD = ""

def main():
    while True:
        # Get the current time
        time_now = datetime.now()

        # Get the ISS position
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()
        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])

        # Get the sunset and sunrise times
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

        # Determine if it is currently night time
        is_night = time_now.hour >= sunset or time_now.hour < sunrise

        # Determine if the ISS is close to the current location
        is_iss_close = (MY_LAT - LOC_BUFFER <= iss_latitude <= MY_LAT + LOC_BUFFER) and (MY_LONG - LOC_BUFFER <= iss_longitude <= MY_LONG + LOC_BUFFER)

        # Print relevant messages
        if is_iss_close and is_night:
            print("Look up! The ISS is above you in the sky.")
            connection = smtplib.SMTP("smtp.gmail.com", 587)
            connection.starttls()
            connection.login(user=EMAIL, password=EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg="Subject:ISS Overhead Alert!\n\nThe ISS is currently overhead. Look up!"
            )
        else:
            print("It is not currently night time or the ISS is not close. Skipping the code.")

        # Sleep for 60 seconds
        time.sleep(60)

if __name__ == "__main__":
    main()