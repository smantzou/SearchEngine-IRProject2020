import threading

from stemmer import *
from nltk.corpus import stopwords
import threading


class Index:
    index_dict = dict()
    count_dict = dict()
    freq_dict = dict()
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

    @staticmethod
    def indexPage(page, threadName):
        print("Thread: " + threadName + " |Indexing page " + str(page[0]))
        urlDict = stemPage(page, Index.stopwords)  # stem the page
        Index.updateIndex(urlDict)  # update the invertedIndex
        Index.updateCounter()
        Index.updateFrequency()

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
        new_counter = return_count_dict()
        for key in new_counter.keys():
            Index.lock.acquire()
            try:
                Index.count_dict.update({key: new_counter.get(key)})
            finally:
                Index.lock.release()

    @staticmethod
    def updateFrequency():
        new_freq_dict = return_freq()
        for key in new_freq_dict.keys():
            Index.lock.acquire()
            try:
                Index.freq_dict.update({key: new_freq_dict.get(key)})
            finally:
                Index.lock.release()

    @staticmethod
    def saveIndex():
        dict_to_file(Index.index_dict, 'Indexer/invertedIndex.pkl')
        dict_to_file(Index.count_dict, 'Indexer/countDict.pkl')
        dict_to_file(Index.freq_dict, 'Indexer/freq_dictionary.pkl')
