import requests
from threading import Lock
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; mma-elo-scraper/1.0)'}

class PageCache:
    def __init__(self):
        self.cached_pages = {}
        self._lock = Lock()

    def cache_page(self, url):
        with self._lock:
            if url in self.cached_pages:
                return
            # Mark in-progress so a second thread doesn't double-fetch
            self.cached_pages[url] = None

        page_content = b'<html></html>'
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            page_content = r.content
        except Exception as e:
            print("Failed making request to", url, '-', e)

        with self._lock:
            self.cached_pages[url] = BeautifulSoup(page_content, 'html.parser')

    def get_page(self, url):
        self.cache_page(url)
        with self._lock:
            return self.cached_pages[url]
