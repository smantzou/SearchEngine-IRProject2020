import sys
import threading
from queue import Queue
from query import *
from stemmer import stemQuery
from timeit import default_timer as timer
import multiprocessing

""" This function create threads-workers that will be used later"""


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
        Query.calculateTF_IDF(document)
        queue.task_done()


"""This function create a queue with pages, it will be use by threads """


def create_jobs():
    for relDoc in relevantDocuments.keys():
        queue.put(relDoc)


"""Here we specify the number of threads that will be used with respect of the number of cores"""


#
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



#
# if __name__ == '__main__':
#     TOP_K_RESULTS = int(sys.argv[1])
#     NUMBER_OF_THREADS = int(sys.argv[2])
#     # NUMBER_OF_THREADS= numberOfThreads()
#     print(NUMBER_OF_THREADS, "number of threads")
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
#
#     Query.returnTopKResults(TOP_K_RESULTS)
#     end = timer()
#     print('Elapsed time : ' + str(end - start))

# WE HAVE THE UNINVERTED INDEX
# MAKE THREADS FIND THE TF IDF OF EVERY URL
# THEN MAKE THREADS FIND THE COS SIM OF EVERY URL
# SORT AND PRINT THE TOP K
