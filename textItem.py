class textItem:
    url = ''
    textList = list()

    def __init__(self, url, textList):
        self.url = url
        self.textList = textList

    def print_TextList(self):
        for str in self.textList:
            print(str)
    def print_url(self):
        print(self.url)