from WikiScraper.Components.BaseTable import BaseTable
from Helpers.DateHelper import DateHelper

class HistoryTable(BaseTable):
    def __init__(self, soup):
        self.history_table = self.get_history_table_from_soup(soup)
        self.date_helper = DateHelper()
        self.col_indices = self._parse_col_indices()

    def get_history_table_from_soup(self, soup):
        # Wikipedia now wraps section headings in <div class="mw-heading mw-heading2">.
        # Find that div by locating the heading element with the MMA record id or text.
        mma_heading_div = None

        heading = soup.find(id='Mixed_martial_arts_record')
        if heading is not None:
            parent = heading.parent
            mma_heading_div = parent if parent.name == 'div' else heading
        else:
            for tag in soup.find_all(['h2', 'h3', 'h4']):
                if 'Mixed martial arts record' in tag.get_text():
                    parent = tag.parent
                    mma_heading_div = parent if parent.name == 'div' else tag
                    break

        if mma_heading_div is None:
            return None

        required_headers = {'Res.', 'Opponent', 'Method', 'Event', 'Date'}
        for sibling in mma_heading_div.find_next_siblings():
            # Stop when the next major section starts
            if sibling.name == 'div' and 'mw-heading2' in sibling.get('class', []):
                break
            if sibling.name == 'table' and 'wikitable' in sibling.get('class', []):
                headers = {th.get_text().strip() for th in sibling.find_all('th')}
                if required_headers.issubset(headers):
                    return sibling

        return None

    def _parse_col_indices(self):
        if self.history_table is None:
            return {}
        header_row = self.history_table.find('tr')
        if header_row is None:
            return {}
        return {th.get_text().strip(): i for i, th in enumerate(header_row.find_all('th'))}

    def _col(self, name):
        return self.col_indices.get(name, -1)

    def get_results_from_history_table(self):
        results = []
        col = self._col('Res.')
        if col < 0:
            return results
        for row in self.history_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) == 0:
                results.append('Incomplete')
            else:
                results.append(cells[col].get_text().strip())
        return results

    def get_opponents_from_history_table(self, wiki_scraper):
        opponents = []
        col = self._col('Opponent')
        if col < 0:
            return opponents
        for row in self.history_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) <= col:
                opponents.append('Incomplete')
            else:
                opponents.append(self.get_fighter_name_from_cell(cells[col], wiki_scraper))
        return opponents

    def get_methods_from_history_table(self):
        methods = []
        col = self._col('Method')
        if col < 0:
            return methods
        for row in self.history_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) <= col:
                methods.append('Incomplete')
            else:
                methods.append(cells[col].get_text().strip())
        return methods

    def get_times_from_history_table(self):
        def extract_date(text):
            date = self.date_helper.reformat_date(text)
            return date if date is not None else 'Incomplete'

        col = self._col('Date')
        if col < 0:
            return []

        dates = []
        rows = self.history_table.find_all('tr')[1:]
        row_index = 0
        while row_index < len(rows):
            cells = rows[row_index].find_all('td')
            if len(cells) <= col:
                dates.append('Incomplete')
                row_index += 1
                continue
            date_text = cells[col].get_text().strip()
            rowspan = int(cells[col].get('rowspan', 1))
            for _ in range(rowspan):
                dates.append(extract_date(date_text))
            row_index += rowspan

        return dates

    def get_event_tiers_from_history_table(self):
        col = self._col('Event')
        if col < 0:
            return []

        events = []
        rows = self.history_table.find_all('tr')[1:]
        row_index = 0
        while row_index < len(rows):
            cells = rows[row_index].find_all('td')
            if len(cells) <= col:
                events.append('Incomplete')
                row_index += 1
                continue
            event_text = cells[col].get_text().strip()
            rowspan = int(cells[col].get('rowspan', 1))
            for _ in range(rowspan):
                events.append(event_text)
            row_index += rowspan

        return events

    def get_matches_from_history_table(self, wiki_scraper):
        if self.history_table is None:
            return []

        results = self.get_results_from_history_table()
        events = self.get_event_tiers_from_history_table()
        opponents = self.get_opponents_from_history_table(wiki_scraper)
        methods = self.get_methods_from_history_table()
        dates = self.get_times_from_history_table()

        matches = []
        for i in range(len(opponents)):
            matches.append({
                'opponent': opponents[i],
                'result': results[i],
                'method': methods[i],
                'date': dates[i],
                'event': events[i],
            })
        return matches

    def get_urls_for_opponents(self, wiki_scraper):
        if self.history_table is None:
            return {}

        col = self._col('Opponent')
        if col < 0:
            return {}

        opponent_urls = {}
        for row in self.history_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) <= col:
                continue
            a_tag = cells[col].find('a')
            if a_tag is None:
                continue
            opponent_url = 'https://en.wikipedia.org' + a_tag['href']
            opponent_name = wiki_scraper.get_fighter_name(opponent_url)
            if opponent_name is None:
                opponent_name = cells[col].get_text().strip()
            opponent_urls[opponent_name] = opponent_url

        return opponent_urls
