import sys
import threading
from queue import Queue
from query import *
from stemmer import stemQuery
from timeit import default_timer as timer

NUMBER_OF_THREADS = 4


def create_workers():
    for n in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=calculateTF_IDF)
        t.daemon = True
        t.start()


def calculateTF_IDF():
    while not queue.empty():
        document = queue.get()
        Query.calculateTF_IDF(document)
        queue.task_done()


def create_jobs():
    for relDoc in relevantDocuments.keys():
        queue.put(relDoc)


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


# if __name__ == '__main__':
#     TOP_K_RESULTS = int(sys.argv[1])
#     NUMBER_OF_THREADS = int(sys.argv[2])
#     QUERY = sys.argv[3:]
#     start = timer()
#     queue = Queue()
#     QUERY = stemQuery(QUERY)
#     Query(QUERY)
#     relevantDocuments = Query.unInvertIndex()
#     if relevantDocuments.__len__() == 0:
#         print("No Documents have the query!")
#         os._exit(1)
#     create_jobs()
#     create_workers()
#     queue.join()
#     Query.returnTopKResults(TOP_K_RESULTS)
#     end = timer()
#     print('Elapsed time : ' + str(end - start))
