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