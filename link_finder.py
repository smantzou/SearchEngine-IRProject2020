from bs4 import BeautifulSoup
from urllib import parse
from domain import isAllowed


class LinkFinder:
    # here must be changes

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, html_string):
        soup = BeautifulSoup(html_string, 'lxml')
        for a in soup.find_all('a', href=True):
            if isAllowed(parse.urljoin(self.base_url, a['href'])):
                self.links.add(parse.urljoin(self.base_url, a['href']))

    def return_url_text(self, html_string):
        soup = BeautifulSoup(html_string, 'lxml')
        strList = list()
        for str in soup.stripped_strings:
            strList.append(str)

        return strList

    def error(self, message):
        pass

    def page_links(self):
        return self.links
