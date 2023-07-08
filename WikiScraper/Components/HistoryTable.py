from datetime import datetime

class HistoryTable:
    def __init__(self, soup):
        self.history_table = self.get_history_table_from_soup(soup)
    
    def get_history_table_from_soup(self, soup):
        tables = soup.find_all('table', class_='wikitable')
        for table in tables:
            headers = table.find_all('th')
            must_have_headers = {
                'Res.': False,
                'Record': False,
                'Opponent': False,
                'Method': False,
                'Event': False,
                'Date': False,
                'Round': False,
                'Time': False,
                'Location': False
            }

            for header in headers:
                header_text = header.text.strip()
                must_have_headers[header_text] = True
            
            incomplete = False
            for header in must_have_headers.keys():
                if must_have_headers[header] == False:
                    incomplete = True
                    break
            try:
                if("Mixed martial arts record" not in table.previous_sibling.previous_sibling.previous_sibling.previous_sibling.text):
                    incomplete = True
            except:
                incomplete = True

            if not incomplete:
                return table
                
        return None
    
    def get_results_from_history_table(self):
        results = []
        rows = self.history_table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            if(len(cells) == 0):
                results.append("Incomplete")
            else:
                results.append(cells[0].text.strip())
        return results

    def get_opponents_from_history_table(self, wiki_scraper):
        opponents = []
        rows = self.history_table.find_all('tr')[1:]
        for row in rows:

            cells = row.find_all('td')
            if(len(cells) < 3):
                opponents.append("Incomplete")
            else:
                a_tag = cells[2].find('a')
                if(a_tag is None):
                    opponents.append(cells[2].text.strip())
                    continue

                opponent_name = wiki_scraper.get_fighter_name('https://en.wikipedia.org' + a_tag['href'])

                if opponent_name is None:
                    opponent_name = cells[2].text.strip()
                
                opponents.append(opponent_name)
        return opponents
    
    def get_methods_from_history_table(self):
        methods_of_victory = []
        rows = self.history_table.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            if(len(cells) == 0):
                methods_of_victory.append("Incomplete")
            else:
                methods_of_victory.append(cells[3].text.strip())
        return methods_of_victory

    def get_times_from_history_table(self):
        def extract_date_from_text(text):
            possible_formats = ["%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%Y"]
            if "(airdate)" in text:
                text = text.replace(" (airdate)", "")
            for possible_format in possible_formats:
                try:
                    fight_date = datetime.strptime(text, possible_format)
                    return fight_date.strftime("%Y-%m-%d")
                except:
                    pass
            return "Incomplete"
    
        dates = []
        rows = self.history_table.find_all('tr')[1:]
        row_index = 0
        while row_index < len(rows):
            row = rows[row_index]
            cells = row.find_all('td')
            if(len(cells) < 6):
                dates.append("Incomplete")
            date_text = cells[5].text.strip()
            rowspan = 1
            if cells[5].has_attr('rowspan'):
                rowspan = int(cells[5]['rowspan'])
            for i in range(rowspan):
                dates.append(extract_date_from_text(date_text))
            row_index += rowspan

        return dates
    
    def get_event_tiers_from_history_table(self):
        events = []
        rows = self.history_table.find_all('tr')[1:]
        row_index = 0
        while row_index < len(rows):
            row = rows[row_index]
            cells = row.find_all('td')
            if(len(cells) < 5):
                events.append("Incomplete")
            event_text = cells[4].text.strip()
            rowspan = 1
            if cells[4].has_attr('rowspan'):
                rowspan = int(cells[4]['rowspan'])
            for i in range(rowspan):
                events.append(event_text)
            row_index += rowspan

        return events
        
    def get_matches_from_history_table(self, wiki_scraper):
        if self.history_table is None:
            return []
        
        matches = []

        results = self.get_results_from_history_table()
        events = self.get_event_tiers_from_history_table()
        opponents = self.get_opponents_from_history_table(wiki_scraper)
        methods_of_victory = self.get_methods_from_history_table()
        dates = self.get_times_from_history_table()

        for i in range(len(opponents)):
            matches.append({
                'opponent': opponents[i], 
                'result': results[i], 
                'method': methods_of_victory[i],
                'date': dates[i], 
                'event': events[i]})
            
        return matches

    def get_urls_for_opponents(self, wiki_scraper):
        if self.history_table is None:
            return []
        
        opponent_urls = {}

        rows = self.history_table.find_all('tr')[1:]
        for row in rows:

            cells = row.find_all('td')
            if(len(cells) < 3):
                continue
            a_tag = cells[2].find('a')
            if(a_tag is None):
                continue

            opponent_url = 'https://en.wikipedia.org' + a_tag['href']
            opponent_name = wiki_scraper.get_fighter_name(opponent_url)
            if opponent_name is None:
                opponent_name = cells[2].text.strip()
                
            opponent_urls[opponent_name] = opponent_url

        return opponent_urls