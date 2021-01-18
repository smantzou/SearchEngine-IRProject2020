from stemmer import stemDictionary, return_UrlDict, return_freq, return_count_dict
from general import *


def initIndexProcess(numberOfIndexes):
    stemDictionary(numberOfIndexes)
    url_dict = return_UrlDict()
    global index_dict
    index_dict = loadIndexFileToDict('Indexer/invertedIndex.pkl')
    indexDict(url_dict, 'Indexer/invertedIndex.pkl')
    if os.path.isfile('Indexer/countDict.pkl'):
        count_dict = loadIndexFileToDict('Indexer/countDict.pkl')
    else:
        count_dict = dict()
    update_counter(count_dict)

    update_frequency()


def update_counter(counter):
    new_counter = return_count_dict()
    for key in new_counter.keys():
        counter.update({key: new_counter.get(key)})
    dict_to_file(counter, 'Indexer/countDict.pkl')


def update_frequency():
    old_freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
    freq_dict = return_freq()
    for key in freq_dict.keys():
        old_freq_dict.update({key: freq_dict.get(key)})
    dict_to_file(old_freq_dict, 'Indexer/freq_dictionary.pkl')


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
