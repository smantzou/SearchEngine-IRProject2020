from stemmer import stemDictionary, return_UrlDict
from general import *


def initIndexProcess(numberOfIndexes):
    stemDictionary(numberOfIndexes)
    url_dict = return_UrlDict()
    global index_dict
    index_dict = loadIndexFileToDict('Indexer/invertedIndex.pkl')
    indexDict(url_dict, 'Indexer/invertedIndex.pkl')


def indexDict(url_dict, file):
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


def loadIndexFileToDict(file):
    index_dict = file_to_dict(file)
    return index_dict


def printIndex():
    for key in index_dict:
        print(key + '-->' + str(index_dict.get(key)))
