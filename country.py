from conf import url


class Country:
    def __init__(self, id, name, last_update=None):
        self.id = id
        self.name = name

    def __init__(self, dict):
        self.id = dict.get('CountryID')
        self.name = dict.get('CountryName')

    def serialize(self, dao):
        serialize_dict = {}
        for key in self.__dict__:
            if self.__dict__[key] is not None:
                serialize_dict[key] = self.__dict__[key]

        if 'CountryID' in serialize_dict:
            serialize_dict['link'] = '{0}/countries/{1}'.format(url, self.id)
        return serialize_dict

    @staticmethod
    def field_to_database_column():
        return {'id': 'CountryID', 'name': 'CountryName', 'CountryID': 'CountryID', 'CountryName': 'CountryName'}