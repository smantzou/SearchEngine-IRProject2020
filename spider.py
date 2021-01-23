from urllib.request import urlopen
from urllib import parse
from textItem import *
from link_finder import LinkFinder
from general import *


class Spider:
    # Class variable (shared among all instances)

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    dict_file = ''
    queue = set()
    crawled = set()
    textDict = dict()
    dictCount = 0

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.dict_file = Spider.project_name + '/dictionary.pkl'
        self.boot()
        Spider.textDict = file_to_dict(Spider.dict_file)

        Spider.dictCount = Spider.textDict.__len__()
        self.crawl_page('First Spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " crawling " + page_url)
            print('Queue: ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            if page_url in Spider.queue:
                Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):

        html_string = ''
        try:

            response = urlopen(page_url)
            if response.getheader('Content-Type').split(';')[0] == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.handle_starttag(html_string)
            aTextItem = textItem(parse.urljoin(Spider.base_url, page_url), finder.return_url_text(html_string))
            Spider.textDict.update({Spider.dictCount: aTextItem})

            Spider.dictCount += 1
        except Exception as ex:
            print(ex)
            print('Error : can not crawled page ' + parse.urljoin(Spider.base_url, page_url))
            return set()

        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        dict_to_file(Spider.textDict, Spider.dict_file)
