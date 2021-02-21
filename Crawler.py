import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sys
import os
import time
import numpy


def create_workers():
    """In this function we create the threads, threads are focus on pre_work function with the parameter of jobs"""
    array = jobsPerThread(MAX_NUMBER_OF_CRAWLS)
    for n in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=pre_work, args=(array[n],))
        t.daemon = True
        t.start()


def jobsPerThread(crawls):
    """This function returns an array with number of gobs that every thread separately must do """
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


def pre_work(k):
    """The first and the last function that threads saw"""
    work(k)
    time.sleep(5)
    os._exit(0)


def work(k):
    """Here the threads do the main job, threads gets on url page from queue,
     after crawl the page and remove it from queue"""
    for i in range(k):
        url = fifo_queue.get()
        Spider.crawl_page(threading.Thread().name, url)
        fifo_queue.task_done()


def create_jobs():
    """This function update the fifo_queue with the next pages that will be crawled """
    for link in file_to_set(QUEUE_FILE):
        fifo_queue.put(link)
    fifo_queue.join()
    crawl()

#
# def create_jobs_best():
#     i = 0
#     queue_links = file_to_set(QUEUE_FILE)
#     while i < MAX_NUMBER_OF_CRAWLS and len(queue_links) > 0:
#         print(i,"i am hereeeeeeee")
#         queue_links = file_to_set(QUEUE_FILE)
#         print(str(len(queue_links)) + 'links in the queue')
#         for link in file_to_set(QUEUE_FILE):
#             fifo_queue.put(link)
#             i += 1
#         fifo_queue.join()



def crawl():
    """If queue_links file has pages then update then fifo_queue"""
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + 'links in the queue')
        create_jobs()


if __name__ == '__main__':
    """The main takes as arguments from command line,with this order:
    the link of first page that we will crawl-> string, the number of crawls that user wants->int,
     keep or not old files-> int(0,1), number of threads to use -> int. Here we create the directory of files.
     terminal must be like: crawler https://www.geeksforgeeks.org/ 100 1 4 """
    PROJECT_NAME = 'Crawler'
    HOMEPAGE = sys.argv[1]
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    DICT_FILE = PROJECT_NAME + '/dictionary.pkl'
    TITLE_DICT = PROJECT_NAME + '/titleDict.pkl'
    NUMBER_OF_THREADS = int(sys.argv[4])
    MAX_NUMBER_OF_CRAWLS = int(sys.argv[2]) - 1
    keep_old_files = bool(int(sys.argv[3]))
    if keep_old_files is False:
        delete_data_files(PROJECT_NAME)
    jobs_per_thread = MAX_NUMBER_OF_CRAWLS // NUMBER_OF_THREADS
    fifo_queue = Queue()
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
    create_workers()
    # crawl()
    create_jobs_best()
