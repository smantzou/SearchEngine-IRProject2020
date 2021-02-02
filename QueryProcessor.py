import sys
import threading
from queue import Queue
from query import *
from stemmer import stemQuery


def create_workers():
    for n in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=calculateTF_IDF)
        t.daemon = True
        t.start()


def calculateTF_IDF():
    pass


def create_jobs():
    for relDoc in relevantDocuments:
        queue.put(relDoc)


if __name__ == '__main__':
    TOP_K_RESULTS = int(sys.argv[1])
    NUMBER_OF_THREADS = int(sys.argv[2])
    QUERY = sys.argv[3:]
    queue = Queue()
    QUERY = stemQuery(QUERY)
    Query(QUERY)
    relevantDocuments = Query.unInvertIndex()
    if relevantDocuments.__len__() == 0:
        print("No Documents have the query!")
        os._exit(1)
    print(relevantDocuments)
    # create_jobs()
    # queue.join()
    # create_workers()
    # create_jobs()

#WE HAVE THE UNINVERTED INDEX
#MAKE THREADS FIND THE TF IDF OF EVERY URL
#THEN MAKE THREADS FIND THE COS SIM OF EVERY URL
#SORT AND PRINT THE TOP K