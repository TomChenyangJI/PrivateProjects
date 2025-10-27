import requests
# import json
from parse_response import get_weather_info
from config import weather_api_key


def get_weather_detail():
    # https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&lat=22.548602&lon=100.047173&cnt=7&appid={weather_api_key}'

    res = requests.get(url, verify=False)

    res_dict = res.json()

    status_code = res_dict.get('cod')

    weather_detail = ""
    if status_code == 200:
        weather_detail = get_weather_info(res_dict)
    else:
        weather_detail = "The http request failed, there is something wrong, check it manually."

    return weather_detail
