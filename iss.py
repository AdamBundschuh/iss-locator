import requests
from datetime import datetime
import math

MY_LAT = 00.0000
MY_LONG = 00.0000


class Iss:
    def __init__(self):
        self.iss_lat = 0.0
        self.iss_lng = 0.0
        self.sunrise = 0
        self.sunset = 0
        self.time_now = 0
        self.update_info()

    def update_info(self):
        iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
        iss_response.raise_for_status()
        iss_data = iss_response.json()

        self.iss_lat = float(iss_data["iss_position"]["latitude"])
        self.iss_lng = float(iss_data["iss_position"]["longitude"])

        parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }

        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        sun_data = response.json()

        self.sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
        self.sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])
        self.time_now = datetime.utcnow().hour

    def is_nighttime(self):
        return self.sunset <= self.time_now <= self.sunrise

    def in_range(self):
        my_lat_range = (MY_LAT - 5, MY_LAT + 5)
        my_long_range = (MY_LONG - 5, MY_LONG + 5)
        return my_lat_range[0] <= self.iss_lat <= my_lat_range[1] \
            and my_long_range[0] <= self.iss_lng <= my_long_range[1]

    def is_visible(self):
        return self.is_nighttime() and self.in_range()

    def display_info(self):
        print(f"Current hour: {self.time_now}")
        print(f"Nighttime between sunset ({self.sunset}) and sunrise ({self.sunrise})")
        print(f"Current ISS Location: {math.floor(self.iss_lat)} | {math.floor(self.iss_lng)}")
        print("-----------------------------------------")
