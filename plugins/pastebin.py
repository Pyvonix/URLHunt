# URLHunt module for Pastebin

class Pastebin:
    """
    Parse pastebin pages to submit URL
    """
    def __init__(self, url):
        self.pastebin_url = url
        self.request = requests.get(self.pastebin_url)

    def page_exist(self):
        if self.request.status_code == 200:
            return True
        raise Exception("The specified page doesn't exist.")

    def is_raw(self):
        if not '/raw/' in self.pastebin_url:
            pastebin_raw = self.pastebin_url.replace('.com/', '.com/raw/')
            self.request = requests.get(pastebin_raw)
        return True

    def pastebin_result(self):
        if self.page_exist() and self.is_raw():
            for line in self.request.text.split('\n'):
                yield line
