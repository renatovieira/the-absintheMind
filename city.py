from country import Country

class City:
    def __init__(self, id, name, country_id, last_update=None):
        self.id = id
        self.name = name
        self.country_id = country_id
        self.last_update = last_update

    def serialize(self):
        return self.__dict__