import math
import threading
import numpy as np
from nltk.corpus import stopwords
from numpy.linalg import norm

from general import *
import os


class Query:
    index_dict = dict()
    count_dict = dict()
    freq_dict = dict()
    stopwords = set()
    relDoc = dict()
    lock = threading.Lock()
    query = []
    query_TF_IDF = list()
    documentCosSim = dict()
    N = 0

    def __init__(self, query):
        self.boot(query)

    @staticmethod
    def boot(query):
        Query.query = query

        Query.stopwords = set(stopwords.words('english'))
        Query.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Query.count_dict = file_to_dict('Indexer/countDict.pkl')
        Query.freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
        Query.N = Query.freq_dict.__len__()
        Query.relDoc = Query.findRelevantDocuments()
        Query.query_TF_IDF = Query.Query_TF_IDF()

    @staticmethod
    def findRelevantDocuments():
        doc_dict = dict()
        for q in Query.query:
            word_dict = Query.index_dict.get(q)
            if word_dict is not None:
                doc_dict.update({q: word_dict})
        return doc_dict

    @staticmethod
    def Query_TF_IDF():
        Query.query = np.array(Query.query)
        freq = []
        for word in Query.query:
            times = np.where(Query.query == word)
            freq.append(len(times[0]))
        tfIdfList = list()
        maxTF = max(freq)

        for i in range(0, len(Query.query)):
            tf = freq[i] / maxTF
            aDict = Query.relDoc.get(Query.query[i])
            if aDict is None:
                ni = 1
            else:
                ni = len(aDict.keys()) + 1
            idf = math.log(1 + ((Query.N - ni) / ni), 10)
            aTuple = (Query.query[i], tf * idf)
            tfIdfList.append(aTuple)
        tfIdfList = {k: v for k, v in tfIdfList}
        queryArray = np.array(list(tfIdfList.values()))
        return queryArray

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
    def calculateTF_IDF(document):
        url = document
        docuArray = np.zeros(shape=len(Query.query_TF_IDF))
        i = 0
        querySet = set(Query.query)
        for q in querySet:
            if q in Query.index_dict.keys():
                if url in Query.index_dict.get(q).keys():
                    freq_in_doc = Query.index_dict.get(q).get(url)
                else:
                    i += 1
                    continue
            else:
                i += 1
                continue
            TF = math.log(freq_in_doc, 10) + 1
            result = TF
            docuArray[i] = result
            i += 1
        docuLength = Query.count_dict.get(url)
        cosSim = Query.calculateCosSim(docuArray, docuLength)
        Query.updateCosineDict(url, cosSim)

    @staticmethod
    def returnRelevantDocuments():
        return Query.relDoc

    @staticmethod
    def calculateCosSim(docuArray, docuLength):
        cosSim = np.dot(Query.query_TF_IDF, docuArray) / (1 * norm(docuLength))
        return cosSim

    @staticmethod
    def updateCosineDict(url, cosSim):
        # Query.documentCosSim.add((url, cosSim))
        Query.lock.acquire()
        try:
            Query.documentCosSim.update({url: cosSim})
        finally:
            Query.lock.release()

    @staticmethod
    def returnTopKResults(k):
        Query.documentCosSim = {k: v for k, v in
                                sorted(Query.documentCosSim.items(), key=lambda item: item[1], reverse=True)}
        i = 0
        for key in Query.documentCosSim.keys():
            print(key, Query.documentCosSim.get(key))
            i += 1
            if i is k:
                break

    @staticmethod
    def printCosSimDict():
        print(Query.documentCosSim)
