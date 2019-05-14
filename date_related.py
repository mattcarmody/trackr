# Component in trackr
# A particular format of the date is called in many modules.
# This was created to stay DRY.

import datetime

def get_date(offset_days=0):
    day = (datetime.date.today() - datetime.timedelta(days=offset_days)).strftime("%Y-%m-%d")
    return day

def get_date_of_last_entry(cur, table_name):
	cur.execute("SELECT Date FROM {} ORDER BY Date DESC LIMIT 1".format(table_name))
	most_recent_entry = cur.fetchone()
	return most_recent_entry
