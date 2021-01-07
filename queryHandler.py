from general import *
from stemmer import stemQuery
import os


def findRelevantDocuments(query):
    doc_dict = dict()
    for q in query:
        word_dict = index_dict.get(q)
        if word_dict is not None:
            doc_dict.update({q: word_dict})
    return doc_dict


def calculateTF_IDF(query):
    relDoc = findRelevantDocuments(query)
    if relDoc.__len__() is 0:
        print('Nothing was found in the Inverted Index!')
        os._exit(0)
    for key in relDoc.keys():
        for url in relDoc.get(key).keys():


def processQuery(query):
    global index_dict
    global freq_dict
    index_dict = file_to_dict('Indexer/invertedIndex.pkl')
    freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
    calculateTF_IDF(stemQuery(query))
