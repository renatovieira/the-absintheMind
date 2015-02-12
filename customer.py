class Customer:
    def __init__(self, id, stored_id, first_name, last_name, email_id, address_id, active, create_date, last_update=None):
        self.id = id
        self.store_id = stored_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_id = email_id
        self.address_id = address_id
        self.active = active
        self.create_date = create_date
        self.last_update = last_update
        
    def __init__(self, dict):
        self.id = dict.get('CustomerID')
        self.store_id = dict.get('StoreID')
        self.first_name = dict.get('FirstName')
        self.last_name = dict.get('LastName')
        self.email_id = dict.get('EmailID')
        self.address_id = dict.get('AddressID')
        self.active =  dict.get('Active')
        self.create_date = str(dict.get('CreateDate'))
        self.last_update = str(dict.get('LastUpdate'))

    def serialize(self):
        return self.__dict__
