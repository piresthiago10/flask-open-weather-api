from flask import Flask, request, jsonify
from resources.weather import Weather
from resources import validators
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 5 * 60  # five minutes
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
searched_cities = []


def verify_status_code(city_name):
    """Verify if the status code is 200 or 404

    Args:
        city_name (string): name of a specific city

    Returns:
        dict: data of a specific city
    """
    if city_name not in searched_cities:
        # busca cidade na api
        weather = Weather(city_name)
        get_weather, status = weather.get()

        # se retornou uma cidade, adiciona no cache, adicona na lista de cidades
        if status == 200:
            city = get_weather.get('city')
            cache.set(city, get_weather)
            searched_cities.append(city)
            return get_weather

        # se não retornou uma cidade, retorna mensagem de erro
        if status == 404:
            return get_weather


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
@cache.cached()
def get_city_name(city_name):
    """Verify if city_name is a valid string and get
    data of a specific city.

    Args:
        city_name (string): name of a specific city

    Returns:
        dict: data of a specific city
    """
    if validators.city_name_validator(city_name):
        city = verify_status_code(city_name)
    else:
        return {"message": "The city name must have just letters"}

    return city


@app.route("/weather")
def get_cities_number():
    """Verify if the parameter max is a valid number
    and return a dict with n numbers of cities

    Returns:
        dict: cities storaged in the cache
    """
    lasted_cities = []
    max_number = request.args.get('max')
    cities_length = len(searched_cities)

    if validators.max_number_validator(max_number):
        max_number = int(max_number)
        if max_number > cities_length:
            max_number = cities_length
        negative_max_number = int(max_number) * -1
        lasted_cities = searched_cities[negative_max_number:]
    else: 
        return {"message": "The max have to be a number greater than 0"}

    return manage_cached_dict(lasted_cities)


if __name__ == '__main__':
    app.run(debug=True)
