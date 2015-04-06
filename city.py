from conf import *


class City:
    url = read_url()

    def __init__(self, id, name, country_id, last_update=None):
        self.id = id
        self.name = name
        self.country_id = country_id

    def __init__(self, dict):
        self.id = dict.get('CityID')
        self.name = dict.get('CityName')
        self.country_id = dict.get('CountryID')

    def serialize(self, dao):
        serialize_dict = {}
        for key in self.__dict__:
            if key != 'country_id':
                serialize_dict[key] = self.__dict__[key]
        serialize_dict['link'] = '{0}/cities/{1}'.format(City.url, self.id)
        serialize_dict['country'] = dao.find_country_by_id(self.country_id).serialize(dao)
        return serialize_dict

    @staticmethod
    def field_to_database_column():
        return {'id': 'CityID', 'name': 'CityName', 'country_id': 'CountryID',
                'CityID': 'CityID', 'CityName': 'CityName', 'CountryID': 'CountryID'}