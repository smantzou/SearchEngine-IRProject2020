from general import *


def processQuery(query):
    index_dict = file_to_dict('Indexer/invertedIndex.pkl')
    freq_dict = file_to_dict('Indexer/freq_dictionary.pkl')

