# URLHunt module for index

import requests
from bs4 import BeautifulSoup


class Indexor:
    """
    Find all files in a web directory
    """
    def __init__(self, url, log):
        self.url = url.rsplit('/', 1)[0]
        self.html = requests.get(self.url)
        self.logging = log

    @staticmethod
    def define(href):
        return 'Directory' if '/' in href else 'File'

    def get_elements(self):
        """ display directory for verbose mode and only return file """
        soup = BeautifulSoup(self.html.content, 'lxml')
        query = soup.find('ul').find_all('li')
        for entry in query:
            self.logging.info('[{type}] {name}'.format(type=self.define(entry.find('a')['href']), name=entry.find('a').text.strip()))
            if self.define(entry.find('a')['href']) == 'File':
                yield entry.find('a').text

    def index_result(self):
        for element in self.get_elements():
            yield '{url}/{file}'.format(url=self.url , file=element.strip())