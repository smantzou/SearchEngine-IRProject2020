from stemmer import *


class Index:
    index_dict = dict()
    count_dict = dict()
    freq_dict = dict()

    def __init__(self):
        self.boot()

    @staticmethod
    def boot():
        Index.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Index.count_dict = file_to_dict('Indexer/countDict.pkl')
        Index.freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')

    @staticmethod
    def indexPage(page):
        urlDict = stemPage(page)  # stem the page
        Index.indexDict(urlDict)  # update the invertedIndex
        Index.update_counter()
        Index.update_frequency()

    @staticmethod
    def indexDict(url_dict):
        for urlKey in url_dict.keys():
            word_dict = url_dict.get(urlKey)
            for wordKey in word_dict.keys():
                if wordKey in Index.index_dict.keys():
                    Index.index_dict.get(wordKey).update({urlKey: word_dict.get(wordKey)})
                else:
                    Index.index_dict.update({wordKey: {}})
                    v = {urlKey: word_dict.get(wordKey)}
                    Index.index_dict[wordKey] = v

    @staticmethod
    def update_counter():
        new_counter = return_count_dict()
        for key in new_counter.keys():
            Index.count_dict.update({key: new_counter.get(key)})

    @staticmethod
    def update_frequency():
        new_freq_dict = return_freq()
        for key in new_freq_dict.keys():
            Index.freq_dict.update({key: new_freq_dict.get(key)})

    @staticmethod
    def saveIndex():
        dict_to_file(Index.index_dict, 'Indexer/invertedIndex.pkl')
        dict_to_file(Index.count_dict, 'Indexer/countDict.pkl')
        dict_to_file(Index.freq_dict, 'Indexer/freq_dictionary.pkl')

#TO-DO FOR NEXT TIME
#FREQ AND COUNT DICTIONARY MUST COME TO THIS SCRIPT
#AND BE UPDATE FROM HERE