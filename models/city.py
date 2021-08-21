
class CityModel():

    def __init__(self, city, description, temp):
        self.city = city
        self.description = description
        self.temp = temp

    def json(self):
        return {
            'city': self.city,
            'description': self.description,
            'temp': self.temp
        
        }
