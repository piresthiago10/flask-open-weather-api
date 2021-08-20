# Flask Open Weather Api

An application that collects data from [Open Weather Api](https://openweathermap.org/api) caches it for some
configurable time and returns it as a JSON object. Also returns a configurable number of last searched cities.

 # Team:

* **Thiago Pires** - *Backend Developer*;

## System Requirements:

* Python 3.6;
* Flask 2.0.1;
* Flask-Caching 1.10.1

## Project Setup:

1. Download or clone this repository
2. Create the virtual environment:
```
python3 - m venv venv
source venv/bin/activate
```
3. Install the requirements:
```
pip install -r requirements.txt
```
4. Insert your api key in config.ini:
```
[openweathermap]
api="Your API Key here"
```
6. Run the project:
```
python app.py
```

## Run tests:
1. In the virtual environment:
```
python tests_weather.py
```


## Tools

* [Visual Studio Code](https://code.visualstudio.com/)
* [Google Chrome](https://www.google.pt/intl/pt-PT/chrome/?brand=CHBD&gclid=Cj0KCQjwn_LrBRD4ARIsAFEQFKt3kLTIsdU6a-sk3FKsxrhplkKaYNHo6Pt3aRbaEAJ3TK4fZslZmtUaAvHVEALw_wcB&gclsrc=aw)
