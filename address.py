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

    def serialize(self):
        return self.__dict__