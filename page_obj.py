
class Page:
    def __init__(self, items, prev_page, next_page):
        self.items = items
        self.prev_page = prev_page
        self.next_page = next_page

    def serialize(self):
        serialize_dict = {}
        for key in self.__dict__:
            if key is not 'items':
                serialize_dict[key] = self.__dict__[key]
        return serialize_dict

    def return_links(self):
        links_dict = {}
        try:
            links_dict['prev_page'] = self.prev_page
            links_dict['next_page'] = self.next_page
        except:
            return links_dict

        return links_dict


    def __init__(self, items, prev_page=False, next_page=False):
        self.items = items
