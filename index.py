from stemmer import *
from nltk.corpus import stopwords
import threading


class Index:
    """This class is responsible for creation of inverted index,
     position dictionary = from words to number of appearances """
    index_dict = dict()
    position_dict = dict()
    stopwords = set()
    lock = threading.Lock()
    PROJECT_NAME = 'Indexer'

    def __init__(self):
        self.boot()

    @staticmethod
    def boot():
        """The method that boot-load the necessary files"""
        create_project_dir(Index.PROJECT_NAME)
        create_index_files(Index.PROJECT_NAME)
        Index.stopwords = set(stopwords.words('english'))
        Index.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Index.position_dict = file_to_dict('Indexer/position_dict.pkl')

    @staticmethod
    def indexPage(page, threadName):
        """The manipulation of methods that create all the dictionaries """
        print(threadName + " |Indexing page " + str(page[0]))
        wordDict = stemPage(page, Index.stopwords)  # stem the page
        urlDict = dict()
        urlDict.update({page[0]: {}})
        urlDict[page[0]] = wordDict
        if urlDict.values().__len__() == 0:
            return 0
        Index.updatePosition(page[0], wordDict)
        Index.updateIndex(urlDict)  # update the invertedIndex

    @staticmethod
    def updateIndex(urlDict):
        """In this method we update-create the inverted index with urlDict,
        from pages to words and number of appearances"""

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
    def saveIndex():
        """Save all the dictionaries to files"""
        dict_to_file(Index.index_dict, 'Indexer/invertedIndex.pkl')
        dict_to_file(Index.position_dict, "Indexer/position_dict.pkl")


    @staticmethod
    def updatePosition(page, positions):
        """In this method we update the position Dictionary with the already made position dictionary"""

        Index.lock.acquire()
        try:
            Index.position_dict.update({page: positions})
        finally:
            Index.lock.release()
