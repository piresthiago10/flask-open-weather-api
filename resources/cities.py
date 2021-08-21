import configparser

import requests
from flask.json import jsonify
from flask_restful import Resource, request
from models import city

from resources import validators

searched_cities = []


class City(Resource):

    def get_api_key(self):
        """Read the file config.ini and get the api key

        Returns:
            string: api key
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['openweathermap']['api']

    def get_weather_data(self, city_name):
        """Access the weather api

        Args:
            city_name (string): a city name

        Returns:
            json: data about the weather of a specifc city
        """
        api_key = self.get_api_key()
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
            city_name, api_key)
        data = requests.get(url)

        return data.json()

    def kelvin_to_celsius(self, temp):
        """Convert kelvin to celsius

        Args:
            temp (int): temperature in kelvin

        Returns:
            int: temperature in celsius
        """
        temp_celsius = int("{0:.0f}".format(int(temp) - 273.15))
        return temp_celsius

    def get(self, city):
        """Get the data of a specifc city and filter specifc values

        city (string): a city name

        Returns:
            dict, status code: dict with specif values and status code.
        """
        self.weather_data = self.get_weather_data(city)
        if self.weather_data["cod"] == 200:
            city_name = self.weather_data["name"]
            temp = "{0:.0f}".format(self.weather_data["main"]["temp"])
            temp_celsius = self.kelvin_to_celsius(temp)
            description = self.weather_data["weather"][0]["description"]
            searched_cities.append(city_name)
            weather_data = {"city_name": city_name,
                            "temp_celsius": temp_celsius, "description": description}
            return weather_data, 200

        if self.weather_data["cod"] == '404' or validators.city_name_validator(city) == False:
            message = {"message": "Sorry. We couldn't find the specified city."}
            return jsonify(message), 404


class Cities(Resource):

    def cities(self):
        """Return the list of searched cities

        Returns:
            list: searched cities
        """
        return searched_cities

    def get(self):
        """Verify the last searched cities

        Returns:
            [type]: [description]
        """
        lasted_cities = []
        max_number = request.args.get('max')

        if validators.attribute_validator(max_number) and validators.max_number_validator(max_number):
            cities_length = len(searched_cities)
            max_number = int(max_number)
            if max_number > cities_length:
                max_number = cities_length
            negative_max_number = int(max_number) * -1
            lasted_cities = searched_cities[negative_max_number:]
        else:
            message = {"message": "The max has to be a number greater than 0"}
            return jsonify(message), 500

        return lasted_cities, 200
