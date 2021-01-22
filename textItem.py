class textItem:
    url = ''
    textList = list()

    def __init__(self, url, textList):
        self.url = url
        self.textList = textList

    def return_list(self):
        return self.textList

    def return_url(self):
        return self.url
