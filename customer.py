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

    def serialize(self):
        return self.__dict__
