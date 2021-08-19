import configparser
import requests

class Weather():

    def __init__(self, city_name):
        self._city_name = city_name

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

    def get(self):
        """Get the data of a specifc city and filter specifc values

        Returns:
            dict, status code: dict with specif values and status code.
        """
        self.weather_data = self.get_weather_data(self._city_name)
        if self.weather_data["cod"] == 200:
            city = self.weather_data["name"]
            temp = "{0:.0f}".format(self.weather_data["main"]["temp"])
            temp_celsius = self.kelvin_to_celsius(temp)
            description = self.weather_data["weather"][0]["description"]
            weather = {"city": city, "temp": temp_celsius,
                       "description": description}
            return weather, 200

        if self.weather_data["cod"] == '404':
            return {"mesage": "Sorry. We couldn't find the specified city."}, 404
