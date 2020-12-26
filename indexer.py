index_dict = dict()
url_dict = dict()


def updateIndexDict(url):
    pass


def makeUrlDict(url, stemmedTokens):
    for stemmedToken in stemmedTokens:
        if stemmedToken not in url_dict.keys():
            url_dict.update({stemmedToken:1})
        else:
            num_of_app = url_dict.get(stemmedToken)
            url_dict.pop(stemmedToken)
            num_of_app += 1
            url_dict.update({stemmedToken:num_of_app})

    print(url_dict)
    updateIndexDict(url)