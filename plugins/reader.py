# URLHunt module for Local file

import os


class Reader:
    """
    Parse local file to submit URL
    """
    def __init__(self, path):
        self.path_file = path

    def file_exist(self):
        if os.path.isfile(self.path_file):
            return True
        raise Exception("The specified file doesn't exist.")

    def reader_result(self):
        f = open(self.path_file, 'r')
        for line in f.readlines():
            yield line