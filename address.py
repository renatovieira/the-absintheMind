class Address:
    def __init__(self, id, address1, address2, district, postal_code, city_id, country_id, last_update=None):
        self.id = id
        self.address1 = address1
        self.address2 = address2
        self.district = district
        self.postal_code = postal_code
        self.city_id = city_id
        self.country_id = country_id
        self.last_update = last_update

    def serialize(self):
        return self.__dict__