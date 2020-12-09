import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sys
import os
import time


#  create a worker set(will die with main)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=pre_work)
        t.daemon = True
        t.start()


def pre_work():
    work()
    time.sleep(3)
    os._exit(0)


# do the next job in the queue

def work(i=0):
    while i < jobs_per_thread:
        url = queue.get()
        Spider.crawl_page(threading.Thread().name, url)
        queue.task_done()
        i += 1


    # each queued link is a new job


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# check if there are items in the queue, if so crawl them
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + 'links in the queue')
        create_jobs()


if __name__ == '__main__':
    PROJECT_NAME = 'stackoverflow'
    HOMEPAGE = sys.argv[1]
    DOMAIN_NAME = get_domain_name(HOMEPAGE)
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    NUMBER_OF_THREADS = int(sys.argv[4])
    MAX_NUMBER_OF_CRAWLS = int(sys.argv[2])
    keep_old_files = bool(sys.argv[3])
    jobs_per_thread = MAX_NUMBER_OF_CRAWLS / NUMBER_OF_THREADS
    queue = Queue()
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
    create_workers()
    crawl()
