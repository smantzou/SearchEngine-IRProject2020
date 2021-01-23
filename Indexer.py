import threading
from queue import Queue
import time
from index import Index
import sys
from general import *
from timeit import default_timer as timer


def create_workers():
    for n in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=pre_index)
        t.daemon = True
        t.start()


def index():
    while not queue.empty():
        page = queue.get()
        Index.indexPage(page, threading.Thread().name)
        queue.task_done()


def pre_index():
    index()


def create_jobs():
    for page in partialCrawlDict.items():
        queue.put(page)


if __name__ == '__main__':
    PROJECT_NAME = 'Indexer'
    create_project_dir(PROJECT_NAME)
    create_index_files(PROJECT_NAME)
    INDEX_FILE = PROJECT_NAME + 'invertedIndex.pkl'
    MAX_NUMBER_OF_INDEXES = int(sys.argv[1])
    keep_old_files = sys.argv[2]
    NUMBER_OF_THREADS = int(sys.argv[3])
    if keep_old_files is False:
        delete_data_files(PROJECT_NAME)
    start = timer()
    Index()
    crawlDict = file_to_dict('Crawler/dictionary.pkl')
    partialCrawlDict = dict()
    if crawlDict.__len__() == 0:
        print("Crawl Dictionary is Empty ... Please crawl some pages first!")
        os._exit(0)
    if MAX_NUMBER_OF_INDEXES > crawlDict.__len__():
        print("Number of requested indexes is larger than the number of Crawled pages ... Crawl Dictionary will "
              "be empty after indexing ends.")
        MAX_NUMBER_OF_INDEXES = crawlDict.__len__()
    for _ in range(0, MAX_NUMBER_OF_INDEXES):
        crawlItem = crawlDict.popitem()
        crawlItem = crawlItem[1]
        partialCrawlDict.update({crawlItem.return_url(): crawlItem.return_list()})
    dict_to_file(crawlDict, 'Crawler/dictionary.pkl')
    queue = Queue()
    create_jobs()
    create_workers()
    queue.join()
    Index.saveIndex()
    end = timer()
    print('Elapsed time : ' + str(end - start))
