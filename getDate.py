# Component in trackr
# A particular format of the date is called in many modules.
# This was created to stay DRY.

import datetime

def get_date(offset_days=0):
    day = (datetime.date.today() - datetime.timedelta(days=offset_days)).strftime("%Y-%m-%d")
    return day
