from stemmer import stemDictionary, return_UrlDict
from general import *

url_dict = dict()
index_dict = dict()


def initIndexProcess():
    stemDictionary()
    url_dict = return_UrlDict()
    index_dict = file_to_dict('Index/tempIndex.pkl')
    if index_dict.__len__() == 0:
        startIndex(url_dict, 'Index/tempIndex.pkl')
    else:
        print('Updating...')
        updateIndex(url_dict, 'Index/tempIndex.pkl')


def startIndex(url_dict, file):
    for urlkey in url_dict.keys():
        word_dict = url_dict.get(urlkey)
        for wordkey in word_dict.keys():
            if wordkey in index_dict.keys():
                index_dict.get(wordkey).update({urlkey: word_dict.get(wordkey)})
            else:
                index_dict.update({wordkey: {}})
                v = {urlkey: word_dict.get(wordkey)}
                index_dict[wordkey] = v

    dict_to_file(index_dict, file)
    printIndex()


def updateIndex(url_dict, file):
    for urlkey in url_dict.keys():
        for wordkey in url_dict.get(urlkey).keys():
            print(wordkey)
            if wordkey in index_dict.keys():
                if urlkey in index_dict.get(wordkey).keys():
                    if index_dict.get(wordkey).get(urlkey) == url_dict.get(urlkey).get(wordkey):
                        continue
                    else:
                        index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})
                else:
                    index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})
            else:
                index_dict.update({wordkey, index_dict.get(wordkey).update({urlkey, url_dict.get(urlkey).get(wordkey)})})

    dict_to_file(index_dict, file)


def printIndex():
    for key in index_dict:
        print(key + '-->' + str(index_dict.get(key)))


initIndexProcess()
