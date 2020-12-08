from bs4 import BeautifulSoup
from urllib import parse


class LinkFinder:

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, html_string):
        soup = BeautifulSoup(html_string, 'lxml')
        for a in soup.find_all('a', href=True):
            self.links.add(parse.urljoin(self.base_url, a['href']))

    def error(self, message):
        pass

    def page_links(self):
        return self.links
