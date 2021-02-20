from stemmer import *
from nltk.corpus import stopwords
import threading
import multiprocessing


class Index:
    index_dict = dict()
    count_dict = dict()
    freq_dict = dict()
    position_dict = dict()
    stopwords = set()
    lock = threading.Lock()

    def __init__(self):
        self.boot()

    @staticmethod
    def boot():
        Index.stopwords = set(stopwords.words('english'))
        Index.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Index.count_dict = file_to_dict('Indexer/countDict.pkl')
        Index.freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
        Index.position_dict = file_to_dict('Indexer/position_dict.pkl')

    @staticmethod
    def indexPage(page, threadName):
        print(threadName + " |Indexing page " + str(page[0]))
        wordDict = stemPage(page, Index.stopwords)
        urlDict = dict()
        urlDict.update({page[0]: {}})
        urlDict[page[0]] = wordDict
        positionDict = wordDict
        # positionDict = makePositionDict(wordDict)
        if urlDict.values().__len__() == 0:
            return 0
        Index.updatePosition(page[0], positionDict)
        Index.updateIndex(urlDict)  # update the invertedIndex
        Index.updateCounter()
        Index.updateFrequency()


    """In this method we update-create the inverted index with urlDict, from pages to words and number of appearances"""

    @staticmethod
    def updateIndex(urlDict):
        for urlKey in urlDict.keys():
            word_dict = urlDict.get(urlKey)
            for wordKey in word_dict.keys():
                Index.lock.acquire()
                try:
                    if wordKey in Index.index_dict.keys():
                        Index.index_dict.get(wordKey).update({urlKey: word_dict.get(wordKey)})
                    else:
                        Index.index_dict.update({wordKey: {}})
                        v = {urlKey: word_dict.get(wordKey)}
                        Index.index_dict[wordKey] = v
                finally:
                    Index.lock.release()

    @staticmethod
    def updateCounter():
        Index.lock.acquire()
        try:
            new_counter = return_count_dict()
            for key in new_counter.keys():
                Index.count_dict.update({key: new_counter.get(key)})
        finally:
            Index.lock.release()

    @staticmethod
    def updateFrequency():
        Index.lock.acquire()
        try:
            new_freq_dict = return_freq()
            for key in new_freq_dict.keys():
                Index.freq_dict.update({key: new_freq_dict.get(key)})
        finally:
            Index.lock.release()

    @staticmethod
    def saveIndex():
        dict_to_file(Index.index_dict, 'Indexer/invertedIndex.pkl')
        dict_to_file(Index.count_dict, 'Indexer/countDict.pkl')
        dict_to_file(Index.freq_dict, 'Indexer/freq_dictionary.pkl')
        dict_to_file(Index.position_dict, "Indexer/position_dict.pkl")

    """In this method we update the position Dictionary with the already made position dictionary"""
    @staticmethod
    def updatePosition(page, positions):
        Index.lock.acquire()
        try:
            Index.position_dict.update({page: positions})
        finally:
            Index.lock.release()


