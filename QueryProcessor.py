import sys
import threading
from queue import Queue
from query import *
from stemmer import stemQuery
from timeit import default_timer as timer
import multiprocessing

""" This function create threads-workers that will be used later"""

NUMBER_OF_THREADS = multiprocessing.cpu_count() - 3


def create_workers():
    for n in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=calculateTF_IDF)
        t.daemon = True
        t.start()


"""The main function-process that threads do, calculate the TF-IDF of avery page with the query.
The threads stop when the queue is empty"""


def calculateTF_IDF():
    while not queue.empty():
        document = queue.get()
        Query.calculateTFofdocument(document, True)
        queue.task_done()


"""This function create a queue with pages, it will be use by threads """


def create_jobs():
    for relDoc in relevantDocuments.keys():
        queue.put(relDoc)


"""Here we specify the number of threads that will be used with respect of the number of cores"""


def numberOfThreads():
    return multiprocessing.cpu_count()


def processQuery(topKResults, query):
    TOP_K_RESULTS = topKResults
    QUERY = query
    start = timer()
    global queue
    queue = Queue()
    QUERY = stemQuery(QUERY)
    Query(QUERY)
    global relevantDocuments
    relevantDocuments = Query.unInvertIndex()
    if relevantDocuments.__len__() == 0:
        print("No Documents have the query!")
        os._exit(1)
    create_jobs()
    create_workers()
    queue.join()
    end = timer()
    print('Elapsed time : ' + str(end - start))
    return Query.returnTopKResults(TOP_K_RESULTS)


def feedBackQuery(query, topKResults):
    query = Query.feedback(query)
    TOP_K_RESULTS = topKResults
    QUERY = query
    start = timer()
    Query(QUERY)
    relevantDocuments = Query.unInvertIndex()
    if relevantDocuments.__len__() == 0:
        print("No Documents have the query!")
        os._exit(1)
    create_jobs()
    create_workers()
    queue.join()
    end = timer()
    print('Elapsed time : ' + str(end - start))
    return Query.returnTopKResults(TOP_K_RESULTS)
