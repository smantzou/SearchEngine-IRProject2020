from general import *
from stemmer import stemQuery
import os
import math
import numpy as np
from numpy.linalg import norm


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
                print("Error in Frequency Dictionary!")
                quit(1)
                continue

            TF = math.log(freq_in_doc,10)+1
            # ni = len(relDoc.get(key).keys())
            # IDF = math.log(1+(N-ni / ni), 10)
            print("key N ni IDF TF URL")
            print(key, TF, url)
            result = TF
            atuple = (key, result)
            tuple_list.append(atuple)
            doc_dict[url] = tuple_list
    for url in doc_dict.keys():
        doc_dict[url] = Convert(doc_dict.get(url))

    return doc_dict


def Convert(tup):
    di = dict(tup)
    return di


def Query_TF_IDF(query):
    query = np.array(query)
    freq = []
    relDoc = findRelevantDocuments(query)
    for word in query:
        times = np.where(query == word)
        freq.append(len(times[0]))
    tfIdfList = list()
    maxTF = max(freq)

    for i in range(0, len(query)):
        tf = freq[i] / maxTF
        aDict = relDoc.get(query[i])
        if aDict is None:
            print('Not found these word  in web ', query[i], 'so tfidf will be zero')
            ni = 1
        else:
            ni = len(aDict.keys()) + 1
        idf = math.log(1+(N-ni / ni), 10)
        aTuple = (query[i], tf * idf)
        tfIdfList.append(aTuple)
    return tfIdfList


def calculateCosineSim(queryArray, docuArray, ldocument):
    cosSim = np.dot(queryArray, docuArray) / (1 * norm(ldocument))
    return cosSim


def returnTopKResults(query_TFIDF, docu_TFIDF):
    cosineSimilarityDict = dict()
    queryArray = np.array(list(query_TFIDF.values()))
    for url in docu_TFIDF.keys():
        i = 0
        docuArray = np.zeros(shape=len(query_TFIDF))
        wordDict = docu_TFIDF.get(url)
        print()
        print(wordDict, url)
        for query in query_TFIDF.keys():
            if query in wordDict.keys():
                print(wordDict.get(query), "get query")
                docuArray[i] = wordDict.get(query)
            else:
                pass
            i += 1
        print(queryArray, docuArray, 'arrays')
        ldocuVector=count_dict.get(url)
        cosineSimilarityDict.update({url: calculateCosineSim(queryArray, docuArray, ldocuVector)})
    cosineSimilarityDict = {k: v for k, v in
                            sorted(cosineSimilarityDict.items(), key=lambda item: item[1], reverse=True)}
    print(cosineSimilarityDict)
    return cosineSimilarityDict


def processQuery(query):
    global index_dict
    global freq_dict
    global count_dict
    count_dict = file_to_dict("Indexer/countDict.pkl")
    index_dict = file_to_dict('Indexer/invertedIndex.pkl')
    freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')
    query = stemQuery(query)
    docu_TFIDF = calculateTF_IDF(query)
    query_TFIDF = Query_TF_IDF(query)
    query_TFIDF = {k: v for k, v in query_TFIDF}
    topKResults = returnTopKResults(query_TFIDF, docu_TFIDF)
