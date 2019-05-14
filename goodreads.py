# Component of trackr.py - saves data from Goodreads.com
# Requires a user ID and shelf in personal.data

import bs4
import requests

import date_related
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

def insert_goodreads_data(cur, today):
	books_read = scrape_goodreads()
	sql = ''' INSERT INTO goodreads(Date, Count) VALUES (?,?)'''
	new_entry = [today, books_read]
	cur.execute(sql, new_entry[0:2])
	return cur

def check_goodreads(cur):
	last_entry_date = date_related.get_date_of_last_entry(cur, "goodreads")
	today = date_related.get_date()

	if today != last_entry_date[0]:
		cur = insert_goodreads_data(cur, today)
		print("New data added to Goodreads.")
	else:
		print("Goodreads was already updated today.")
	
	return cur
