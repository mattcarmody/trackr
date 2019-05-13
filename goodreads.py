# Component of trackr.py - saves data from Goodreads.com
# Requires a user ID and shelf in personal.data

import bs4
import requests

from getDate import get_date
import personal

def scrape_goodreads():
	bsUrl = "https://www.goodreads.com/review/list/{}?shelf={}".format(personal.data["grUserID"], personal.data["grShelf"])
	res = requests.get(bsUrl)
	res.raise_for_status()
	bsSoup = bs4.BeautifulSoup(res.text, "lxml")
	booksTable = bsSoup.find("table", {"id" : "books"})
	count = -1
	for row in booksTable.findAll("tr"):
		count += 1
	return count

def update_goodreads(cur):
	# Select most recent entry
	cur.execute("SELECT Date FROM goodreads ORDER BY Date DESC LIMIT 1")
	last_entry = cur.fetchone()
	
	# If last entry is not today, scrape and add new data. Else skip.
	today = get_date()
	if today != last_entry[0]:
		books_read = scrape_goodreads()
		sql = ''' INSERT INTO goodreads(Date, Count) VALUES (?,?)'''
		new_entry = [today, books_read]
		cur.execute(sql, new_entry[0:2])
		print("New data added to Goodreads.")
	else:
		print("Goodreads was already updated today.")
	
	return cur
