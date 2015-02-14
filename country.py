class Country:
    def __init__(self, id, name, last_update=None):
        self.id = id
        self.name = name

    def __init__(self, dict):
        self.id = dict.get('CountryID')
        self.name = dict.get('CountryName')

    def serialize(self):
        return self.__dict__