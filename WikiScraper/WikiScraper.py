import requests
from bs4 import BeautifulSoup
from WikiScraper.Components import EventTable, HistoryTable, PageCache
from Helpers.DateHelper import DateHelper

class WikiScraper:
    def __init__(self):
        self.page_cache = PageCache.PageCache()
        self.date_helper = DateHelper()

    def get_infobox(self, wiki_url, fighter_soup=None):
        if fighter_soup is None:
            fighter_soup = self.page_cache.get_page(wiki_url)

        for table in fighter_soup.find_all('table'):
            if 'infobox' in table.get('class', []):
                return table

        return None

    def get_event_matches(self, wiki_url):
        event_soup = self.page_cache.get_page(wiki_url)
        table = EventTable.EventTable(event_soup, self)
        return table.extract_matches()

    def get_matches(self, wiki_url):
        fighter_soup = self.page_cache.get_page(wiki_url)
        table = HistoryTable.HistoryTable(fighter_soup)
        return table.get_matches_from_history_table(self)

    def get_opponent_urls(self, wiki_url):
        fighter_soup = self.page_cache.get_page(wiki_url)
        table = HistoryTable.HistoryTable(fighter_soup)
        return table.get_urls_for_opponents(self)

    def get_fighter_name(self, wiki_url):
        fighter_soup = self.page_cache.get_page(wiki_url)
        title_tag = fighter_soup.find('span', class_='mw-page-title-main')
        if title_tag is None:
            return None
        return title_tag.text.split('(')[0].strip()

    def get_fighter_dob(self, wiki_url):
        infobox = self.get_infobox(wiki_url)
        if infobox is None:
            return None

        # Standard Wikipedia microformat — most reliable
        bday_span = infobox.find('span', class_='bday')
        if bday_span is not None:
            return bday_span.text.strip()  # Already YYYY-MM-DD

        # Fallback: scan Born row text for a year and surrounding words
        def is_four_digit_year(word):
            if len(word) == 4 and word.isdigit():
                year = int(word)
                return 1950 <= year <= 2009
            return False

        for row in infobox.find_all('tr'):
            if 'Born' not in row.text:
                continue
            words = row.prettify().split()
            for i in range(len(words)):
                if not is_four_digit_year(words[i]):
                    continue
                fighter_dob = words[i - 2] + " " + words[i - 1] + " " + words[i]
                return self.date_helper.reformat_date(fighter_dob)

        return None
