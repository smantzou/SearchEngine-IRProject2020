from stemmer import stemDictionary, return_UrlDict
from general import *

url_dict = dict()
index_dict = dict()


def initIndexProcess():
    stemDictionary()
    url_dict = return_UrlDict()
    # index_dict = file_to_dict('Index/tempIndex.pkl')
    updateIndex(url_dict)


def updateIndex(url_dict):
    for urlkey in url_dict.keys():
        for wordkey in url_dict.get(urlkey).keys():
            if wordkey in index_dict.keys():
                if urlkey in index_dict.get(wordkey).keys():
                    if index_dict.get(wordkey).get(urlkey) == url_dict.get(urlkey).get(wordkey):
                        continue
                    else:
                        index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})
                else:
                    index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})
            else:
                index_dict.update(
                    {wordkey, index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})})

    printIndex()


def printIndex():
    for key in index_dict:
        print(key + '-->' + str(index_dict.get(key)))


initIndexProcess()from stemmer import stemDictionary, return_UrlDict
from general import *

url_dict = dict()
index_dict = dict()


def initIndexProcess():
    stemDictionary()
    url_dict = return_UrlDict()
    # index_dict = file_to_dict('Index/tempIndex.pkl')
    updateIndex(url_dict)


def updateIndex(url_dict):
    for urlkey in url_dict.keys():
        for wordkey in url_dict.get(urlkey).keys():
            if wordkey in index_dict.keys():
                if urlkey in index_dict.get(wordkey).keys():
                    if index_dict.get(wordkey).get(urlkey) == url_dict.get(urlkey).get(wordkey):
                        continue
                    else:
                        index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})
                else:
                    index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})
            else:
                index_dict.update(
                    {wordkey, index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})})

    printIndex()


def printIndex():
    for key in index_dict:
        print(key + '-->' + str(index_dict.get(key)))


initIndexProcess()
