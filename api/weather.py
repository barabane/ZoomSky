import os
from urllib import response
from requests import request
from datetime import datetime, timedelta

from database.db import db

class Weather:
    def __init__(self) -> None:
        pass

    def __format_req(self, req_file: str, req_body: str):
        return f"{os.environ.get('API_BASE_URL')}/{req_file}?key={os.environ.get('API_KEY')}&{req_body}&lang=ru"

    def today_weather(self, user_data):
        response = request(method='GET', url=self.__format_req('current.json', f"q={user_data['lat']},{user_data['lon']}"))
        return response.json()
    
    def tomorrow_weather(self, city_name: str):
        response = request(method='GET', url=self.__format_req('forecast.json', f'q={city_name}&date={datetime.today().date() + timedelta(days=1)}'))
        return response.json()['forecast']['forecastday']
    
    def week_weather(self, city_name: str):
        response = request(method='GET', url=self.__format_req('forecast.json', f'q={city_name}&days=5'))
        return response.json()['forecast']['forecastday']
    
    def get_details_of_day(self, date: str, user_id: int):
        city_name = db.get_user(user_id)[3]
        response = request(method='GET', url=self.__format_req('forecast.json', f'q={city_name}&day={date}'))
        return response['forecast']['forecastday'][0]

    
weather = Weather()