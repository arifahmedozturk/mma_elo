import re
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
        
        possible_infobox_classes = ['infobox vcard', 'infobox biography vcard', 'infobox']
        for possible_infobox_class in possible_infobox_classes:
            infobox = fighter_soup.find('table', class_=possible_infobox_class)
            if infobox is not None:
                return infobox
            
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
        title_tag =fighter_soup.find('span', class_="mw-page-title-main")
        if title_tag is None:
            return None
        return title_tag.text.split('(')[0].strip()
    
    def get_fighter_dob(self, wiki_url):
        def is_four_digit_year(word):
            if len(word) == 4 and word.isdigit():
                year = int(word)
                if year >= 1950 and year <= 2005:
                    return True
            return False
        
        infobox = self.get_infobox(wiki_url)
        if infobox is None:
            return None
        infobox_rows = infobox.find_all('tr')
        born_row_words = []
        for row in infobox_rows:
            if "Born" in row.text:
                born_row_words = row.prettify().split()

        for i in range(len(born_row_words)):
            if not is_four_digit_year(born_row_words[i]):
                continue
            fighter_dob = born_row_words[i - 2] + " " + born_row_words[i - 1] + " " + born_row_words[i]
            return self.date_helper.reformat_date(fighter_dob)
        return None
