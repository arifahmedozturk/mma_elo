class BaseTable:
    def get_fighter_name_from_cell(self, cell, wiki_scraper):
        a_tag = cell.find('a')
        if a_tag is None:
            return cell.text.strip()
        name = wiki_scraper.get_fighter_name('https://en.wikipedia.org' + a_tag['href'])
        if name is None:
            return cell.text.strip()
        return name