from flask import Flask, request, jsonify
from resources.weather import Weather
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 5 * 60 # five minutes
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
searched_cities = []

def verify_status_code(city_name):

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

    city = verify_status_code(city_name)

    return city

@app.route("/weather")
def get_cities_number():
    lasted_cities = []
    max_number = request.args.get('max')
    negative_max_number = int(max_number) * -1
    lasted_cities = searched_cities[negative_max_number:]
    return manage_cached_dict(lasted_cities)

if __name__ == '__main__':
    app.run(debug=True)
