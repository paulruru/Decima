from os import (
    getenv
)

from dotenv import (
    load_dotenv
)

import requests




load_dotenv()
USERNAME = getenv("GEO_NAME")


def get_city(city_name):
    # 1. Ищем город
    search_url = "http://api.geonames.org/searchJSON"

    search_params = {
        "q": city_name,      # название города
        "maxRows": 1,        # берем первый результат
        "username": USERNAME
    }

    response = requests.get(search_url, params=search_params)
    data = response.json()

    if not data["geonames"]:
        return False

    city = data["geonames"][0]

    return [city['name'], city["lat"], city["lng"]]


def get_time(lat, lng):
    # 2. Получаем таймзону
    timezone_url = "http://api.geonames.org/timezoneJSON"

    timezone_params = {
        "lat": lat,
        "lng": lng,
        "username": USERNAME
    }

    response = requests.get(timezone_url, params=timezone_params)
    timezone_data = response.json()

    if timezone_data:
        return timezone_data["time"]
    else:
        return False 
