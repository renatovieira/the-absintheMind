from conf import url


class City:
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
            if self.__dict__[key] is not None:
                serialize_dict[key] = self.__dict__[key]

        if self.country_id is not None:
            serialize_dict['country'] = dao.find_country_by_id(self.country_id).serialize(dao)

        if self.id is not None:
            serialize_dict['link'] = '{0}/cities/{1}'.format(url, self.id)
        return serialize_dict

    @staticmethod
    def field_to_database_column():
        return {'id': 'CityID', 'name': 'CityName', 'country_id': 'CountryID',
                'CityID': 'CityID', 'CityName': 'CityName', 'CountryID': 'CountryID'}