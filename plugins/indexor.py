# URLHunt module for index

import requests
from bs4 import BeautifulSoup


class Indexor:
    """
    Find all files in a web directory
    """
    def __init__(self, url, log):
        self.url = url.rsplit('/', 1)[0]
        self.html = BeautifulSoup(requests.get(self.url).content, 'lxml')
        self.indexing_type = {
            'ul': self.html_contains_list,
            'table': self.html_contains_table
        }
        self.logging = log

    @staticmethod
    def define(href):
        return 'Directory' if '/' in href else 'File'

    @staticmethod
    def html_contains_list(html):
        return html.find('ul').find_all('li')

    @staticmethod
    def html_contains_table(html):
        table = html.find('table').find_all('td')
        return filter(lambda row: row.find('a'), table)

    def search(self):
        soup = self.html.find('body').findChildren(recursive=False)
        query = []
        for element in soup:
            if element.name in self.indexing_type:
                query = self.indexing_type[element.name](self.html)
        return query

    def get_elements(self):
        """ display directory for verbose mode and only return file """
        query = self.search()
        for entry in query:
            self.logging.info('[{type}] {name}'.format(type=self.define(entry.find('a')['href']), name=entry.find('a').text.strip()))
            if self.define(entry.find('a')['href']) == 'File':
                yield entry.find('a')['href']

    def index_result(self):
        for element in self.get_elements():
            yield '{url}/{file}'.format(url=self.url , file=element.strip())
