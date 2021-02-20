import threading
from queue import Queue
import queue
from spider import Spider
from domain import *
from general import *
import sys
import os
import time
import numpy


class MyThread(threading.Thread):
    def __init__(self, number, target):
        super(MyThread, self).__init__()
        self.number = number
        self._target = target


def create_workers():
    array = jobsPerThread(MAX_NUMBER_OF_CRAWLS)
    for n in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=pre_work, args=(array[n],))
        t.daemon = True
        threadList.append(t)
        t.start()


def jobsPerThread(crawls):
    jobs = crawls % NUMBER_OF_THREADS
    moreJobs = numpy.zeros(shape=NUMBER_OF_THREADS, dtype=int)
    if jobs != 0:
        i = 0
        while jobs != 0:
            print(jobs)
            moreJobs[i] += 1
            jobs = jobs - 1
            i += 1
    arrayOfJobs = numpy.full(shape=NUMBER_OF_THREADS, fill_value=jobs_per_thread)
    arrayOfJobs = arrayOfJobs + moreJobs
    print(arrayOfJobs, "the final jobs per thread")
    return arrayOfJobs


def pre_work():
    array = jobsPerThread(MAX_NUMBER_OF_CRAWLS)
    for i in array:
        work(i)
    while fifo_queue.empty():
        time.sleep(2)
    print(Spider.dictCount, " number of not crawled pages ")
    time.sleep(5)
    os._exit(0)


# do the next job in the queue

def work(k):
    for i in range(k):
        url = fifo_queue.get()
        Spider.crawl_page(threading.Thread().name, url)
        fifo_queue.task_done()


# each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        fifo_queue.put(link)
    fifo_queue.join()
    crawl()


# check if there are items in the queue, if so crawl them
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + 'links in the queue')
        create_jobs()


if __name__ == '__main__':

    PROJECT_NAME = 'Crawler'
    HOMEPAGE = sys.argv[1]
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    DICT_FILE = PROJECT_NAME + '/dictionary.pkl'
    TITLE_DICT = PROJECT_NAME + '/titleDict.pkl'
    QUEUE = 0
    NUMBER_OF_THREADS = int(sys.argv[4])
    MAX_NUMBER_OF_CRAWLS = int(sys.argv[2])
    keep_old_files = bool(int(sys.argv[3]))
    if keep_old_files is False:
        delete_data_files(PROJECT_NAME)
    jobs_per_thread = MAX_NUMBER_OF_CRAWLS // NUMBER_OF_THREADS
    fifo_queue = Queue(MAX_NUMBER_OF_CRAWLS)
    print(fifo_queue.maxsize, "ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
    # twp = TaskWorkerPool(NUMBER_OF_THREADS)

    create_workers()
    crawl()
    # create_jobs()

# TO DO FOR NEXT TIME
# SOLVE THE PROBLEM OF THE HEURISTIC ALG APPROACH TO CRAWLING
# QUERY PROCESSOR MULTITHREADING BEGIN
