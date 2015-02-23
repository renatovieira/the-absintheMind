
class Page:
    def __init__(self, items, prev_page, next_page):
        self.items = items
        self.prev_page = prev_page
        self.next_page = next_page

    def __init__(self, items, prev_page=False, next_page=False):
        self.items = items
