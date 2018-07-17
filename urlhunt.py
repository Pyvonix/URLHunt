#!/usr/bin/env python3

import argparse
import logging
import requests

from plugins.indexor import Indexor
from plugins.iterator import Iterator
from plugins.pastebin import Pastebin
from plugins.reader import Reader


def config_logging(bol):
    if bol:
         log_level = logging.INFO
    else:
         log_level = logging.WARNING
    logging.basicConfig(level=log_level,
                        format="%(message)s")

def parse_args():
    """ Parse command line """
    parser = argparse.ArgumentParser()
    input_mode = parser.add_mutually_exclusive_group()
    input_mode.add_argument("-u", "--url", help="process with url in input", action="store")
    input_mode.add_argument("-f", "--file", help="process with local file", action="store")
    input_mode.add_argument("-p", "--pastebin", help="process with raw page on pastebin", action="store")
    url_mode_options = parser.add_mutually_exclusive_group()
    url_mode_options.add_argument("-b", "--bruteforce", help="basic iterator to find extra files", action="store_true", default=False)
    url_mode_options.add_argument("-i", "--index", help="list all files in index", action="store_true", default=False)
    parser.add_argument("-s", "--submit", help="submit result on URLHaus", action="store_true", default=False)
    parser.add_argument("-t", "--tag", help="add tag(s) for sumbission process (separator: +)", action="store", default=[])
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
    parser.add_argument("--version", action="version", version="URL Hunt 1.4")
    return parser.parse_args()


class URLhaus:
    """
    Use urlhaus API to reporte compromised url
    """
    abuse_ch = 'https://urlhaus.abuse.ch/api/'
    api_key = 'YOUR_API_KEY'
    headers_abuse_ch = {"Content-Type": "application/json"}

    def jsonData(self, compromised_url, tags):
        return {
                'token': self.api_key,
                'anonymous': '0',
                'submission': [
                    {
                       'threat' : 'malware_download',
                       'url' : host,
                       'tags': tags
                    } for host in compromised_url ]
               }

    def send(self, gen_url, list_tag):
        response = requests.post(self.abuse_ch, json=self.jsonData(gen_url, list_tag), timeout=15, headers=self.headers_abuse_ch)
        for line in response.content.decode('utf8').split('\n'):
            logging.info(line)


class Main(URLhaus):
    """
    Main process to collect url
    """
    def __init__(self, args):
        self.target_url = args.url
        self.tag = args.tag.split('+') if args.tag else args.tag
        self.pastebin_url = args.pastebin
        self.path_file = args.file
        self.bol_submit = args.submit
        self.bol_bruteforce = args.bruteforce
        self.bol_index = args.index

    def default(self):
        r = requests.get(self.target_url)
        if r.status_code == 200:
            yield self.target_url

    def use_url_option_bruteforce(self):
        iterator = Iterator(self.target_url, logging)
        return iterator.iter_result()

    def use_url_option_indexor(self):
        indexor = Indexor(self.target_url, logging)
        return indexor.index_result()

    def select_url_options(self):
        if self.bol_bruteforce:
            return self.use_url_option_bruteforce()
        elif self.bol_index:
            return self.use_url_option_indexor()
        else:
            return self.default()

    def select_pastebin(self):
        pastebin = Pastebin(self.pastebin_url)
        return pastebin.pastebin_result()

    def select_reader(self):
        reader = Reader(self.path_file)
        return reader.reader_result()

    def select_input_mode(self):
        if self.target_url:
            return self.select_url_options()
        elif self.pastebin_url:
            return self.select_pastebin()
        elif self.path_file:
            return self.select_reader()
        else:
            return self.default()

    def process(self):
        elements = list(self.select_input_mode())
        if self.bol_submit:
            logging.warning('[*] Submission...')
            self.send(elements, self.tag)
            logging.warning('[!] Done')
        else:
            logging.warning('[*] Result:')
            for element in elements:
                logging.warning(element)


if __name__ == "__main__":
    args = parse_args()
    config_logging(args.verbose)
    main = Main(args)
    main.process()