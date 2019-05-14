# Component of trackr.py - saves data from Codewars.com
# Requires a username and accesskey in personal.data

import json
import requests

import date_related
import personal

def scrape_codewars():
	cwUrl = "https://www.codewars.com/api/v1/users/{}".format(personal.data["cwUsername"])
	cwResponse = requests.get(cwUrl, auth=("?access_key", personal.data["cwAccessKey"]))
	cwResponse.raise_for_status()
	return json.loads(cwResponse.text)

def track_codewars(cur):
	last_entry_date = date_related.get_date_of_last_entry(cur, "codewars")
	today = date_related.get_date()
	
	if today != last_entry_date[0]:
		cwData = scrape_codewars()
		sql = ''' INSERT INTO codewars(Date, Honor, Points, Challenges) VALUES (?,?,?,?)'''
		new_entry = [today, cwData["honor"], cwData["ranks"]["overall"]["score"], cwData["codeChallenges"]["totalCompleted"]]
		cur.execute(sql, new_entry[0:4])
		print("New data added to Codewars.")
	else:
		print("Codewars was already updated today.")
	
