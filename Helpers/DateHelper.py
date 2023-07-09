from datetime import datetime
from dateutil.relativedelta import relativedelta

class DateHelper:
    def __init__(self):
        pass

    def add_years_to_date(self, date, years):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        new_date_obj = date_obj + relativedelta(years=years)
        new_date = new_date_obj.strftime("%Y-%m-%d")
        return new_date

    def reformat_date(self, date):
        if "(airdate)" in date:
            date = date.replace(" (airdate)", "")
            
        possible_formats = ["(%Y-%m-%d)", "%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%Y"]
        for possible_format in possible_formats:
            try:
                date_object = datetime.strptime(date, possible_format)
                return date_object.strftime("%Y-%m-%d")
            except Exception as e:
                pass
        return None