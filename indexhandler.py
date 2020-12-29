from stemmer import stemDictionary, return_UrlDict
from general import *


# mia methodo poy tha kaleitai otan exoyme ftasei ena sygkekrimeno arithmo megethoys sto temp index
# mia methodo poy tha kanei update ton megalo index
# na diorthwsoyme bugs toy stemmer
# na mhn mpainei o crawler se oti rossoblyat selida briskei aka ban DOMAINS
# ean den mporei na mpei sthn prwth selida poy toy dinetai na pairnei mia allh


def initIndexProcess(tempUpdate, generalUpdate, numberOfIndexes):
    if tempUpdate:
        stemDictionary(numberOfIndexes)
        url_dict = return_UrlDict()
        global index_dict
        index_dict = loadIndexFileToDict('Indexer/tempIndex.pkl')
        indexDict(url_dict, 'Indexer/tempIndex.pkl')
    if generalUpdate:
        pass


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
