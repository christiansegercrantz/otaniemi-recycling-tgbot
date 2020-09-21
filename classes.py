class Item:
    def __init__(self):
        self.myname = ""
        self.mydesc = ""
        self.myprice = 0
        self.myphotos = []
        pass

    def name(self, name):
        self.myname = name

    def desc(self, desc):
        self.mydesc = desc

    def price(self, price):
        self.myprice = price

    def photo(self, photo, caption):
        self.myphotos.append((photo,caption))

    def clear(self):
        self.myname = ""
        self.mydesc = ""
        self.myprice = 0
        self.myphotos = []

    def __str__(self):
    	return 'Name: {self.myname}\nDescription: {self.mydesc}\nPrice: {self.myprice}'.format(self=self)
