import math
import threading
import numpy as np
from nltk.corpus import stopwords
from numpy.linalg import norm
import multiprocessing
from general import *
import os

"""This class is responsible for calculating the similarity of the documents with the query"""


class Query:
    index_dict = dict()
    count_dict = dict()
    freq_dict = dict()
    stopwords = set()
    relDoc = dict()
    lock = multiprocessing.Lock()
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
            Query.relDoc = Query.findRelevantDocuments(query)
            Query.unInvertedIndex = Query.unInvertIndex()
            Query.query_TF_IDF_Dict = query  # the query is allready in tf terms

    @staticmethod
    def boot(query):
        Query.query = query
        Query.stopwords = set(stopwords.words('english'))
        Query.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Query.count_dict = file_to_dict('Indexer/countDict.pkl')
        Query.freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
        Query.positionDict = file_to_dict('Indexer/position_dict.pkl')
        Query.N = Query.freq_dict.__len__()
        if Query.N == 0:
            print("nothing in inverted index ")

        Query.query_TF_IDF_Dict = Query.Query_TF_IDF()
        Query.relDoc = Query.findRelevantDocuments(Query.query_TF_IDF_Dict)
        Query.unInvertedIndex = Query.unInvertIndex()

    """This static method returns a part of inverted index only with these words tha query has """

    @staticmethod
    def findRelevantDocuments(queryDocument):
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
    def Query_TF_IDF():
        queryDict = dict()
        Query.query = np.array(Query.query)
        freq = []
        for word in Query.query:
            times = np.where(Query.query == word)
            freq.append(len(times[0]))
        tfIdfList = list()
        maxTF = max(freq)

        for i in range(0, len(Query.query)):
            # tf = freq[i] / maxTF
            aDict = Query.relDoc.get(Query.query[i])
            if aDict is None:
                ni = 1
            else:
                ni = len(aDict.keys()) + 1
            tf = freq[i]
            tf = np.log(tf) + 1
            idf = np.log(1 + (Query.N / ni))
            queryDict.update({Query.query[i]: tf * idf})

        return queryDict

    """This function invert the already inverted index, so it returns a dictionary from documents to a dict with
    words-number of appearances, with this function we know all the documents-pages that is relevant with the query"""

    @staticmethod
    def unInvertIndex():
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
            doc_dict[url] = Query.Convert(doc_dict.get(url))

        return doc_dict

    def Convert(tuplet):
        di = dict(tuplet)
        return di

    @staticmethod
    def calculateTFofdocument(url, flag):
        wordDict = Query.positionDict.get(url)
        tfDict = dict()
        for word in wordDict.keys():
            wordNum = wordDict.get(word)
            wordNum = np.log(wordNum) + 1
            tfDict.update({word: wordNum})
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
        notLiketf = dict()
        negativeDectionary = dict()
        theNewQuery = dict()
        query = Query.query_TF_IDF_Dict
        for word in query:
            query.update({word: query.get(word) * aParameter})
        alist = []
        for documents in pageFeedback:
            if documents.value() == 1:
                alist.append(documents)

        for a in alist:
            wordDict = Query.calculateTFofdocument(a, False)
            if pageFeedback.get(a) == 1:
                likedTf.update({a: wordDict})
            else:
                notLiketf.update({a: wordDict})

        likedDocuments = len(likedTf.keys())
        notLikedDocuments = len(notLiketf.keys())
        # add the liked pages
        positiveDictionary = Query.dictoparetor(likedTf, positiveDictionary, likedDocuments, bParameter)
        negativeDictionary = Query.dictoparetor(notLiketf, negativeDectionary, notLikedDocuments, gParameter)

        for word in negativeDictionary.keys():
            if positiveDictionary.get(word) is None:
                pass
            else:
                result = positiveDictionary.get(word) - negativeDictionary.get(word)
                if result > 0:
                    theNewQuery.update({word: result})
        return theNewQuery

    @staticmethod
    def dictoparetor(oldDict, newDict, size, parameter):
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
