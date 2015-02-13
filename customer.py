class Customer:
    def __init__(self, id, stored_id, first_name, last_name, email_id, address_id, active, create_date, last_update=None):
        self.id = id
        self.store_id = stored_id
        self.name = Name(first_name, last_name)
        self.email_id = email_id
        self.address_id = address_id
        self.active = active
        self.create_date = create_date
        self.last_update = last_update
        
    def __init__(self, dict):
        self.id = dict.get('CustomerID')
        self.store_id = dict.get('StoreID')
        self.name = Name(dict.get('FirstName'), dict.get('LastName'))
        self.email_id = dict.get('EmailID')
        self.address_id = dict.get('AddressID')
        self.active =  dict.get('Active')
        self.create_date = str(dict.get('CreateDate'))
        self.last_update = str(dict.get('LastUpdate'))

    def serialize(self):
        self.name = self.name.serialize()
        return self.__dict__


class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def serialize(self):
        return self.__dict__
