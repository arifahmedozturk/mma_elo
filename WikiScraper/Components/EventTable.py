from WikiScraper.Components.BaseTable import BaseTable
from Helpers.DateHelper import DateHelper

class EventTable(BaseTable):
    def __init__(self, soup, wiki_scraper):
        self.date_helper = DateHelper()

        self.event_table = soup.find('table', class_='toccolours')
        self.wiki_scraper = wiki_scraper

        self.event_name = self.get_event_name(soup)
        self.event_date = self.get_event_date(soup)
    
    def get_event_name(self, soup):
        return soup.find('h1', id='firstHeading').text.strip()
    
    def get_event_date(self, soup):
        infobox = self.wiki_scraper.get_infobox("", soup)
        infobox_rows = infobox.find_all("tr")
        for infobox_row in infobox_rows:
            row_title = infobox_row.find("th")
            if row_title is None:
                continue

            if row_title.text.strip() == "Date":
                date = infobox_row.find("td")
                if date is None:
                    continue

                date_text = date.find('span').text.strip()
                return self.date_helper.reformat_date(date_text)
            
        return None

    def extract_matches(self):
        if self.event_table is None:
            return []
        
        matches = []
        rows = self.event_table.find_all('tr')
        for row in rows:
            if 'weight' not in row.text:
                continue

            cells = row.find_all('td')
            if len(cells) < 6:
                continue

            fighter = self.get_fighter_name_from_cell(cells[1], self.wiki_scraper)
            opponent = self.get_fighter_name_from_cell(cells[3], self.wiki_scraper)
            method = cells[4].text.strip()

            matches.append({
                'fighter': fighter,
                'opponent': opponent,
                "result": "Win",
                'method': method,
                'event': self.event_name,
                'date': self.event_date
            })
    
        return matches