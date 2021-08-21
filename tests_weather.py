import unittest

from werkzeug.wrappers import response

from app import app, cache


class WeatherTest(unittest.TestCase):
    def setUp(self):
        app.config['Testing'] = True
        app.config['Debug'] = False
        self.app = app.test_client()

    def test_get_city(self):
        response = self.app.get("/weather/boston")
        cache.set("boston", response.json)
        self.assertEqual(response.json, cache.get("boston"))

    def test_get_invalid_city(self):
        response = self.app.get("/weather/boston7")
        message = {'message': "Sorry. We couldn't find the specified city."}
        self.assertEqual(response.json, message)

    def test_get_nowhere_city(self):
        response = self.app.get("/weather/neverland")
        message = {'message': "Sorry. We couldn't find the specified city."}
        self.assertEqual(response.json, message)

    def test_attribute(self):
        response = self.app.get("/weather/boston")
        response = self.app.get("/weather/texas")
        response = self.app.get("/weather/rio de janeiro")
        response = self.app.get("/weather/lisboa")
        response = self.app.get("/weather/rome")
        response = self.app.get("/weather/lima")
        lima = cache.get("Lima")
        lisbon = cache.get("Lisbon")
        rome = cache.get("Rome")
        response = self.app.get("/weather?max=3")
        cities = {'Lima': lima, 'Lisbon': lisbon, 'Rome': rome}
        self.assertEqual(response.json, cities)

    def test_attribute_greater_value(self):
        response = self.app.get("/weather/lisboa")
        response = self.app.get("/weather/rome")
        response = self.app.get("/weather/lima")
        lima = cache.get("Lima")
        lisbon = cache.get("Lisbon")
        rome = cache.get("Rome")
        boston = cache.get("Boston")
        rio_de_janeiro = cache.get("Rio de Janeiro")
        texas = cache.get("Texas")
        response = self.app.get("/weather?max=10")

        cities = {'Lima': lima, 'Lisbon': lisbon, 'Rome': rome,
                   'Boston': boston, "Rio de Janeiro": rio_de_janeiro, "Texas": texas}
        self.assertEqual(response.json, cities)

    def test_negative_attribute_value(self):
        response = self.app.get("/weather?max=-3")
        message = {'message': 'The max has to be a number greater than 0'}
        self.assertEqual(response.json, message)

    def test_wrong_attribute_value(self):
        response = self.app.get("/weather?max=two")
        message = {'message': 'The max has to be a number greater than 0'}
        self.assertEqual(response.json, message)

    def test_wrong_attribute(self):
        response = self.app.get("/weather?maxx=3")
        message = {"message": "The max has to be a number greater than 0"}
        self.assertEqual(response.json, message)


if __name__ == "__main__":
    unittest.main()
