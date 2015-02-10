class Country:
    def __init__(self, id, name, last_update=None):
        self.id = id
        self.name = name
        self.last_update = last_update

    def serialize(self):
        return self.__dict__