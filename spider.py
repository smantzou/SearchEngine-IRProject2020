from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
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
    title_file = ''
    queue = set()
    crawled = set()
    textDict = dict()
    titleDict = dict()
    dictCount = 0
    countOfNotCrawledPgages = 0
    crawledPages = 0
    bannedResponses = ['application', 'image', 'xml']

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.dict_file = Spider.project_name + '/dictionary.pkl'
        Spider.title_file = Spider.project_name + '/titles.pkl'
        self.boot()
        Spider.textDict = file_to_dict(Spider.dict_file)
        Spider.titleDict = file_to_dict(Spider.title_file)
        if Spider.textDict.__len__() == 0:
            Spider.dictCount = 1
        else:
            Spider.dictCount = list(Spider.textDict.keys())[-1] + 1
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
            Spider.crawledPages += 1
            Spider.update_files()

    @staticmethod
    def returnCrawled():
        return Spider.crawledPages

    @staticmethod
    def gather_links(page_url):
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type').split('/')[0] in Spider.bannedResponses:
                raise Exception("Invalid Response")
            if response.getheader('Content-Type').split('/')[1] in Spider.bannedResponses:
                raise Exception("Invalid Response")
            if response.getheader('Content-Type').split(';')[0] == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                soup = BeautifulSoup(html_string, 'html.parser')
                title = soup.find('title')
                title = title.text
                finder = LinkFinder(Spider.base_url, page_url)
                finder.handle_starttag(html_string)
                aTextItem = textItem(parse.urljoin(Spider.base_url, page_url), finder.return_url_text(html_string))
                Spider.textDict.update({Spider.dictCount: aTextItem})
                Spider.titleDict.update({page_url: title})
                Spider.dictCount += 1
                return finder.page_links()
        except Exception as ex:
            print(ex)
            print('Error : can not crawled page ' + parse.urljoin(Spider.base_url, page_url))
            if page_url not in Spider.crawled:
                Spider.countOfNotCrawledPgages += 1
            return set()

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
        dict_to_file(Spider.titleDict, Spider.title_file)
