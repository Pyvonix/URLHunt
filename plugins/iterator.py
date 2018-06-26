# URLHunt module for iteration

import requests
from itertools import chain


class Iterator:
    """
    Try to find available url based on given url
    """
    def __init__(self, url, log):
        self.host = url.rsplit('.', 1)[0][:-1]
        self.extension = '.' + url.rsplit('.', 1)[1]
        self.logging = log

    def iter_number(self):
        """ Iteration between 0 and 21 """
        self.logging.info('Number iteration...')
        for n in range(0, 21):
            if requests.get(self.host + str(n) + self.extension).status_code == 200:
                self.logging.info(self.host + str(n) + self.extension)
                yield self.host + str(n) + self.extension

    def iter_capital(self):
        """ Iteration between A and Z """
        self.logging.info('Maj iteration...')
        for c in range(65, 91):
            if requests.get(self.host + chr(c) + self.extension).status_code == 200:
                self.logging.info(self.host + chr(c) + self.extension)
                yield self.host + chr(c) + self.extension

    def iter_minuscule(self):
        """ Iteration between a and z """
        self.logging.info('Min iteration...')
        for m in range(97, 123):
            if requests.get(self.host + chr(m) + self.extension).status_code == 200:
                self.logging.info(self.host + chr(m) + self.extension)
                yield self.host + chr(m) + self.extension

    def iter_result(self):
        for res in chain(self.iter_number(), self.iter_capital(), self.iter_minuscule()):
            yield res