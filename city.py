from country import Country

class City:
    def __init__(self, id, name, country_id):
        self.id = id
        self.name = name
        self.country_id = country_id

    def serialize(self):
        return self.__dict__