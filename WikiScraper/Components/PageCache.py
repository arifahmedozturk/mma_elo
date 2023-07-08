import requests
from bs4 import BeautifulSoup

class PageCache:
    def __init__(self):
        self.cached_pages = {}

    def cache_page(self, url):
        if self.cached_pages.get(url) is not None:
            return
        page_content = "<html> </html?>"
        try:
            r = requests.get(url)
            page_content = r.content
        except:
            print("Failed making request to", url)
        self.cached_pages[url] = BeautifulSoup(page_content, 'html.parser')
            

    def get_page(self, url):
        self.cache_page(url)
        return self.cached_pages.get(url)
    