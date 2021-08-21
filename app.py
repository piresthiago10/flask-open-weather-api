from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_restful import Api, Resource

from resources import validators
from resources.cities import City, Cities
from models import city as city_model

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 5 * 60  # five minutes
}

app = Flask(__name__)
api = Api(app)
app.config.from_mapping(config)
cache = Cache(app)

def manage_cached_dict(last_cities):
    """Verify if each searched city is in cache, them 
    storage it in a dict 

    Args:
        last_cities (list): list with the lasted searched cities

    Returns:
        dict: data of cached cities
    """
    cached_cities = {}

    for city in last_cities:
        if cache.get(city):
            cached_cities[city] = cache.get(city)
        else:
            last_cities.remove(city)
            if city in cached_cities.keys():
                cached_cities.pop(city)

    return cached_cities

@app.route("/weather/<string:city_name>")
def city(city_name):

    if cache.get(city_name):
        return cache.get(city_name)


    city = City()
    weather_data, status = city.get(city_name)

    if status == 404:
        return weather_data

    if status == 200:
        city_name = weather_data.get('city_name')
        temp_celsius = weather_data.get('temp_celsius')
        description = weather_data.get('description')
        city_weather = city_model.CityModel(city_name, temp_celsius, description)
        cache.set(city_name, city_weather.json())

    return city_weather.json(), 200

@app.route("/weather")
def cities():
    cities = Cities()
    get_cities, status = cities.get()

    if status == 500:
        return get_cities
        
    return jsonify(manage_cached_dict(get_cities)), 200

if __name__ == '__main__':
    app.run(debug=True)
