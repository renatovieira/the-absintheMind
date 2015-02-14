from country import Country

class City:
    def __init__(self, id, name, country_id, last_update=None):
        self.id = id
        self.name = name
        self.country_id = country_id

    def __init__(self, dict):
        self.id = dict.get('CityID')
        self.name = dict.get('CityName')
        self.country_id = dict.get('CountryID')

    def serialize(self):
        return self.__dict__

    @staticmethod
    def field_to_database_column():
        return {'id': 'CityID', 'name': 'CityName', 'country_id': 'CountryID'}