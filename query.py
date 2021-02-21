import threading
import numpy as np
from nltk.corpus import stopwords
from numpy.linalg import norm
from general import *

"""This class is responsible for calculating the similarity of the documents with the query"""


class Query:
    index_dict = dict()
    stopwords = set()
    relDoc = dict()
    lock = threading.Lock()
    query = []
    query_TF_IDF_Dict = dict()
    documentCosSim = dict()
    unInvertedIndex = dict()
    positionDict = dict()
    N = 0
    """The constructor load all the necessary files tha will be used for cosine similarity. 
    here it calculated the TI-IDF value of quarry"""

    def __init__(self, query):
        if query.__class__ is list:
            self.boot(query)
        else:
            Query.relDoc = Query.find_relevant_documents(query)
            Query.unInvertedIndex = Query.un_invert()
            Query.query_TF_IDF_Dict = query  # the query is already in tf terms

    @staticmethod
    def boot(query):
        Query.query = query
        Query.stopwords = set(stopwords.words('english'))
        Query.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Query.positionDict = file_to_dict('Indexer/position_dict.pkl')
        Query.N = Query.positionDict.__len__()
        if Query.N == 0:
            print("nothing in inverted index ")

        Query.query_TF_IDF_Dict = Query.query_tf_idf()
        Query.relDoc = Query.find_relevant_documents(Query.query_TF_IDF_Dict)
        Query.unInvertedIndex = Query.un_invert()

    """This static method returns a part of inverted index only with these words tha query has """

    @staticmethod
    def find_relevant_documents(queryDocument):
        doc_dict = dict()
        for q in queryDocument.keys():
            word_dict = Query.index_dict.get(q)
            if word_dict is not None:
                doc_dict.update({q: word_dict})
        return doc_dict

    """This static method calculate the TF-IDF of query. First we calculate the max frequency of a word,
    later the Terms frequency and last the IDF. Returns an array of TF*IDF terms with size equal to query, one
    for every word"""

    @staticmethod
    def query_tf_idf():
        queryDict = dict()
        Query.query = np.array(Query.query)
        freq = []
        for word in Query.query:
            times = np.where(Query.query == word)
            freq.append(len(times[0]))

        for i in range(0, len(Query.query)):
            aDict = Query.relDoc.get(Query.query[i])
            if aDict is None:
                ni = 1
            else:
                ni = len(aDict.keys()) + 1
            tf = freq[i]  # just tf of terms
            tf = np.log(tf) + 1
            idf = np.log(1 + (Query.N / ni))
            queryDict.update({Query.query[i]: tf * idf})

        return queryDict

    """This function invert the already inverted index, so it returns a dictionary from documents to a dict with
    words-number of appearances, with this function we know all the documents-pages that is relevant with the query"""

    @staticmethod
    def un_invert():
        doc_dict = dict()
        for key in Query.relDoc.keys():
            for url in Query.relDoc.get(key).keys():
                doc_dict.update({url: list()})

        for key in Query.relDoc.keys():
            for url in Query.relDoc.get(key).keys():
                tuple_list = doc_dict.get(url)
                aTuple = (key, Query.relDoc.get(key).get(url))
                tuple_list.append(aTuple)
                doc_dict[url] = tuple_list
        for url in doc_dict.keys():
            doc_dict[url] = Query.convert(doc_dict.get(url))

        return doc_dict

    @staticmethod
    def convert(tupleItem):
        di = dict(tupleItem)
        return di

    @staticmethod
    def calculate_tf(url, flag):

        wordDict = Query.positionDict.get(url)
        tfDict = dict()
        for word in wordDict.keys():
            wordNum = wordDict.get(word)
            TF = np.log(wordNum) + 1
            aDict = Query.relDoc.get(word)
            if aDict is None:
                ni = 1
            else:
                ni = len(aDict.keys()) + 1
            idf = np.log(1 + (Query.N / ni))

            tfDict.update({word: TF * idf})
        if flag:
            cosSim = Query.calculateCosSim(Query.query_TF_IDF_Dict, tfDict)
            Query.updateCosineDict(url, cosSim)
        return tfDict

    """Here we calculate the Terms frequency of common words in a document and query """

    """Method that returns the relevant documents with the query"""

    @staticmethod
    def returnRelevantDocuments():
        return Query.relDoc

    """Here it calculated the cosine similarity of two vectors, one vector represent the query and the other the 
    document """

    @staticmethod
    def calculateCosSim(queryDict, documentDict):
        dot = 0
        for word in queryDict.keys():
            inside = documentDict.get(word)
            if inside is None:
                pass
            else:
                dot = dot + queryDict.get(word) * documentDict.get(word)
        arrayTF = np.array(list(documentDict.values()))
        result = dot / (1 * norm(arrayTF))
        return result

    @staticmethod
    def feedback(pageFeedback):
        aParameter = 1
        bParameter = 0.5
        gParameter = 0.3
        positiveDictionary = dict()
        likedTf = dict()
        notLiked = dict()
        negativeDictionary = dict()
        theNewQuery = dict()
        query = Query.query_TF_IDF_Dict
        for word in query:
            query.update({word: query.get(word) * aParameter})
        list_with_top_k = []
        for documents in pageFeedback:
            list_with_top_k.append(documents)

        for a in list_with_top_k:
            wordDict = Query.calculate_tf(a, False)
            if pageFeedback.get(a) == 1:
                likedTf.update({a: wordDict})
            else:
                notLiked.update({a: wordDict})

        likedDocuments = len(likedTf.keys())
        notLikedDocuments = len(notLiked.keys())
        # add the liked pages
        positiveDictionary = Query.dict_operator(likedTf, positiveDictionary, likedDocuments, bParameter)
        negativeDictionary = Query.dict_operator(notLiked, negativeDictionary, notLikedDocuments, gParameter)

        for word in negativeDictionary.keys():
            if positiveDictionary.get(word) is None:
                pass
            else:
                result = positiveDictionary.get(word) - negativeDictionary.get(word)
                if result > 0:
                    theNewQuery.update({word: result})
        return theNewQuery

    @staticmethod
    def dict_operator(oldDict, newDict, size, parameter):
        for doc in oldDict.keys():
            for word in oldDict.get(doc):
                if newDict.get(word) is None:
                    newDict.update({word: oldDict.get(doc).get(word) * parameter})
                else:
                    oldTF = oldDict.get(doc).get(word)
                    new = newDict.get(word)
                    newDict.update({word: (oldTF + new) * parameter})

        for word in newDict.keys():
            newDict.update({word: newDict.get(word) / size})
        return newDict

    """We store every cosine similarity of every page with the query at a dictionary, important is """

    @staticmethod
    def updateCosineDict(url, cosSim):
        Query.lock.acquire()
        try:
            Query.documentCosSim.update({url: cosSim})
        finally:
            Query.lock.release()

    "With the already made cosine similarity dict, we sort and return the top K most relevant documents"

    @staticmethod
    def returnTopKResults(k):
        Query.documentCosSim = {k: v for k, v in
                                sorted(Query.documentCosSim.items(), key=lambda item: item[1], reverse=True)}
        topKDict = dict()
        i = 0
        for key in Query.documentCosSim.keys():
            topKDict.update({i + 1: key})
            i += 1
            if i is k:
                break
        return topKDict

    @staticmethod
    def printCosSimDict():
        print(Query.documentCosSim)
