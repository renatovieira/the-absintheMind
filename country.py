class Country:
    def __init__(self, id, name, last_update=None):
        self.id = id
        self.name = name

    def __init__(self, dict):
        self.id = dict.get('CountryID')
        self.name = dict.get('CountryName')

    def serialize(self, dao):
        serialize_dict = self.__dict__
        serialize_dict['link'] = 'http://localhost:5000/countries/q/id={0}'.format(self.id)
        return serialize_dict

    @staticmethod
    def field_to_database_column():
        return {'id': 'CountryID', 'name': 'CountryName'}