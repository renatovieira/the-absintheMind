from conf import url


class Address:
    def __init__(self, id, address1, address2, district, postal_code, city_id, country_id, last_update=None):
        self.id = id
        self.address1 = address1
        self.address2 = address2
        self.district = district
        self.postal_code = postal_code
        self.city_id = city_id
        self.country_id = country_id

    def __init__(self, dict):
        self.id = dict.get('AddressID')
        self.address1 = dict.get('Address1')
        self.address2 = dict.get('Address2')
        self.district = dict.get('District')
        self.postal_code = dict.get('PostalCode')
        self.city_id = dict.get('CityID')
        self.country_id = dict.get('CountryID')

    def serialize(self, dao):
        serialize_dict = {}
        for key in self.__dict__:
            if self.__dict__[key] is not None:
                serialize_dict[key] = self.__dict__[key]

        if self.city_id is not None:
            serialize_dict['city'] = dao.find_city_by_id(self.city_id).serialize(dao)

        if self.id is not None:
            serialize_dict['link'] = '{0}/addresses/{1}'.format(url, self.id)
        return serialize_dict

    @staticmethod
    def field_to_database_column():
        return {'id': 'AddressID', 'address1': 'Address1', 'address2': 'Address2',
                'district': 'District', 'postal_code': 'PostalCode', 'city_id': 'CityID', 'country_id': 'CountryID',
                'AddressID': 'AddressID', 'Address1': 'Address1', 'Address2': 'Address2',
                'District': 'District', 'PostalCode': 'PostalCode', 'CityID': 'CityID', 'CountryID': 'CountryID'}