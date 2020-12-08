import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'wikipedia'
HOMEPAGE = 'https://www.wikipedia.org/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 16
print("beast gamiesai")
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


#  create a worker set(will die with main)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# do the next job in the queue

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.Thread().name, url)
        queue.task_done()


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


create_workers()
crawl()
