# Component of trackr.py - saves data from Duolingo.com
# Requires a username in personal.data

import json
import requests

import date_related
import personal

def scrape_duolingo():
	duoUrl = "https://www.duolingo.com/users/{}".format(personal.data["duoUsername"])
	duoResponse = requests.get(duoUrl)
	duoResponse.raise_for_status()
	return json.loads(duoResponse.text)

def update_duolingo(cur):    
	# Select most recent entry
	cur.execute("SELECT Date FROM duolingo ORDER BY Date DESC LIMIT 1")
	last_entry = cur.fetchone()
	
	# If last entry is not today, add new data. Else skip.
	today = date_related.get_date()
	if today != last_entry[0]:
		duoData = scrape_duolingo()
		sql = ''' INSERT INTO duolingo(Date, Greek, Esperanto, Vietnamese, Italian, Welsh, Irish, Czech, Indonesian, Spanish, Chinese, Russian, Portuguese, Norwegian, Turkish, Romanian, Polish, Dutch, French, German, HighValyrian, Korean, Danish, Hungarian, Japanese, Hebrew, Swahili, Swedish, Ukrainian) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
		new_entry = [today]
		for i in range(len(duoData["languages"])):
			new_entry.append(duoData["languages"][i]["points"])
		cur.execute(sql, new_entry[0:29])
		print("New data added to Duolingo.")
	else:
		print("Duolingo was already updated today.")
