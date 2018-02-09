# Component in trackr
# A particular format of the date is called in many modules.
# This was created to stay DRY.

import datetime

def get_date():
    today = datetime.date.today().strftime("%m/%d/%y")
    return today
