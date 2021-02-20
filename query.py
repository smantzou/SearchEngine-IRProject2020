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
    query_TF_IDF = list()
    documentCosSim = dict()
    unInvertedIndex = dict()
    positionDict = dict()
    N = 0
    """The constructor load all the necessary files tha will be used for cosine similarity. 
    here it calculated the TI-IDF value of quarry"""

    def __init__(self, query):
        # self.boot(query)
        Query.query = query
        Query.stopwords = set(stopwords.words('english'))
        Query.index_dict = file_to_dict('Indexer/invertedIndex.pkl')
        Query.count_dict = file_to_dict('Indexer/countDict.pkl')
        Query.freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
        Query.positionDict = file_to_dict('Indexer/position_dict.pkl')
        Query.N = Query.freq_dict.__len__()
        Query.relDoc = Query.findRelevantDocuments()
        Query.query_TF_IDF = Query.Query_TF_IDF()
        Query.unInvertedIndex = Query.unInvertIndex()

    """This static method returns a part of inverted index only with these words tha query has """

    @staticmethod
    def findRelevantDocuments():
        doc_dict = dict()
        for q in Query.query:
            word_dict = Query.index_dict.get(q)
            if word_dict is not None:
                doc_dict.update({q: word_dict})
        return doc_dict

    """This static method calculate the TF-IDF of query. First we calculate the max frequency of a word,
    later the Terms frequency and last the IDF. Returns an array of TF*IDF terms with size equal to query, one
    for every word"""

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
            # tf = freq[i] / maxTF
            aDict = Query.relDoc.get(Query.query[i])
            if aDict is None:
                ni = 1
            else:
                ni = len(aDict.keys()) + 1
            tf = freq[i]
            idf = np.log(1 + (Query.N / ni))

            aTuple = (Query.query[i], tf * idf)
            tfIdfList.append(aTuple)
        tfIdfList = {k: v for k, v in tfIdfList}
        queryArray = np.array(list(tfIdfList.values()))
        return queryArray

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
    def calculateTF(url):
        positions = Query.positionDict.get(url).values()
        # freq_in_doc = Query.index_dict.get(q).get(url)
        docuWords = list(positions)
        fWords = []
        for i in docuWords:
            fWords.append(tuple(i)[1])
        arrayOFtf = np.array(fWords)
        arrayOFtf = np.log(arrayOFtf)
        arrayOFtf = arrayOFtf + 1
        print(arrayOFtf, "after  log")

        return arrayOFtf

    """Here we calculate the Terms frequency of common words in a document and query """

    @staticmethod
    def calculateTF_IDF(document):
        # Here we have dict from url to wordDict
        url = document
        # docuArray = np.zeros(shape=len(Query.query_TF_IDF))
        arrayOfTf = Query.calculateTF(url)
        wordDict = Query.positionDict.get(url)

        # i = 0
        # querySet = set(Query.query)
        # for q in querySet:
        #     if q in Query.index_dict.keys():
        #         if url in Query.index_dict.get(q).keys():
        #             freq_in_doc = Query.index_dict.get(q).get(url)
        #             print(freq_in_doc,q,"h lekseiiii ")
        #         else:
        #             i += 1
        #             continue
        #     else:
        #         i += 1
        #         continue
            # TF = math.log(freq_in_doc, 10) + 1
            # result = TF
            # docuArray[i] = result

        cosSim = Query.calculateCosSim(Query.Query_TF_IDF(), arrayOfTf, wordDict)
        Query.updateCosineDict(url, cosSim)

    """Method that returns the relevant documents with the query"""

    @staticmethod
    def returnRelevantDocuments():
        return Query.relDoc

    """Here it calculated the cosine similarity of two vectors, one vector represent the query and the other the 
    document """

    @staticmethod
    def calculateCosSim(query_TFIDF, docuTFarray, wordsINDocument):
        query=set(Query.query)
        wordsINquery = np.array(query)
        queryArray = np.zeros(shape=(len(docuTFarray),), dtype=float)
        i = 0
        for termTF in query_TFIDF:
            queryArray[i] = termTF
            i += 1
        print(query_TFIDF)
        # protes leksis me tf meta midenika

        dotProduct = 0
        i = 0
        for word in wordsINquery:
            if word in wordsINDocument:
                tupleOfword = word.valeus()

                # take the tf of term tha is in docu and query
                if i < len(wordsINquery):
                    wordTuple = wordsINDocument.get(word)
                    wordTF = wordTuple[1]  # take the tf of this word
                    positionInquery = np.where(wordsINquery == word)
                    position = positionInquery[0]
                    print(wordsINquery[position], word, queryArray[position], wordTF, "hereeeeeeeeee")
                    dotProduct += np.dot(queryArray[position], wordTF)
                else:
                    break

        cosSim = dotProduct / 1 * norm(docuTFarray)
        print(norm(docuTFarray), "normaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        # cosSim = np.dot(Query.query_TF_IDF, docuTFarray) / (1 * norm(docuTFarray))
        return cosSim

    """We store every cosine similarity of every page with the query at a dictionary """

    @staticmethod
    def updateCosineDict(url, cosSim):
        # Query.documentCosSim.add((url, cosSim))
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
        i = 0
        for key in Query.documentCosSim.keys():
            print(key, Query.documentCosSim.get(key))
            i += 1
            if i is k:
                break

    @staticmethod
    def printCosSimDict():
        print(Query.documentCosSim)
