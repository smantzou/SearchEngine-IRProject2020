from general import *
from stemmer import stemQuery
import os
import numpy as np
import math


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

    N = len(freq_dict)
    for key in relDoc.keys():
        for url in relDoc.get(key).keys():
            doc_dict.update({url: list()})

    for key in relDoc.keys():
        for url in relDoc.get(key).keys():
            tuple_list = doc_dict.get(url)
            freq_in_doc = relDoc.get(key).get(url)
            max_freq = freq_dict.get(url)
            TF = freq_in_doc / max_freq
            ni = len(relDoc.get(key).keys())
            IDF = math.log(N / ni)
            print(IDF)
            result = TF * IDF
            atuple = {key: result}
            tuple_list.append(atuple)
            doc_dict[url]=tuple_list
    return doc_dict


def processQuery(query):
    global index_dict
    global freq_dict
    index_dict = file_to_dict('Indexer/invertedIndex.pkl')
    freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
    calculateTF_IDF(stemQuery(query))
    dict = calculateTF_IDF(query)
    print(dict)
