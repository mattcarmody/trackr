import datetime

def get_log_time():
	current_dt = datetime.datetime.now()
	yr_month = current_dt.strftime("%Y_%m")
	day = current_dt.strftime("%d")
	file_name = current_dt.strftime("log_%H_%M_%S.txt")
	return yr_month, day, file_name

def get_date(offset_days=0):
    day = (datetime.date.today() - datetime.timedelta(days=offset_days)).strftime("%Y-%m-%d")
    return day

def get_date_of_last_entry(cur, table_name):
	cur.execute("SELECT Date FROM {} ORDER BY Date DESC LIMIT 1".format(table_name))
	most_recent_entry = cur.fetchone()
	return most_recent_entry
