# Component in trackr
# A particular format of the date is called in many modules.
# This was created to stay DRY.

import datetime

def get_date():
    today = "=DATE({})".format(datetime.date.today().strftime("%Y,%-m,%-d"))
    return today
