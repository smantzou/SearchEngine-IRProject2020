from general import *
from stemmer import stemQuery
import os
import math
import numpy as np


def findRelevantDocuments(query):
    doc_dict = dict()
    for q in query:
        word_dict = index_dict.get(q)
        if word_dict is not None:
            doc_dict.update({q: word_dict})
    return doc_dict


def calculateTF_IDF(query):
    relDoc = findRelevantDocuments(query)
    if relDoc.__len__() == 0:
        print('Nothing was found in the Inverted Index!')
        os._exit(0)
    doc_dict = dict()
    global N
    N = len(freq_dict)
    for key in relDoc.keys():
        for url in relDoc.get(key).keys():
            doc_dict.update({url: list()})

    for key in relDoc.keys():
        for url in relDoc.get(key).keys():
            tuple_list = doc_dict.get(url)
            freq_in_doc = relDoc.get(key).get(url)
            max_freq = freq_dict.get(url)
            if max_freq is None:
                continue
            TF = freq_in_doc / max_freq
            ni = len(relDoc.get(key).keys())
            IDF = math.log(N / ni, 10)
            result = TF * IDF
            atuple = {key: result}
            tuple_list.append(atuple)
            doc_dict[url] = tuple_list
    return doc_dict


def Query_TF_IDF(query):
    query = np.array(query)
    print(query)
    freq = []
    relDoc = findRelevantDocuments(query)

    for word in query:
        times = np.where(query == word)
        freq.append(len(times[0]))
    tfIdfList = list()
    mafTF = max(freq)
    for i in range(0, len(query)):
        tf = freq[i] / mafTF

        ni = len(relDoc.get(query[i]).keys())

        idf = math.log(N / ni, 10)
        print(idf)
        aTuple = {query[i]: tf*idf}
        tfIdfList.append(aTuple)
    return tfIdfList


def processQuery(query):
    global index_dict
    global freq_dict
    index_dict = file_to_dict('Indexer/invertedIndex.pkl')
    freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
    calculateTF_IDF(stemQuery(query))
    dict = calculateTF_IDF(query)
    query_TFIDF = Query_TF_IDF(query)
    print(query_TFIDF)
