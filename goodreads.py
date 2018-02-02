# Component of trackr.py - saves data from Goodreads.com
# Requires a user ID and shelf in personal.data

import bs4
import datetime
import requests

import personal

def update_Goodreads(wb):
    
    bsUrl = "https://www.goodreads.com/review/list/{}?shelf={}".format(personal.data["grUserID"], personal.data["grShelf"])
    res = requests.get(bsUrl)
    res.raise_for_status()
    bsSoup = bs4.BeautifulSoup(res.text, "lxml")
    booksTable = bsSoup.find("table", {"id" : "books"})
    count = -1
    for row in booksTable.findAll("tr"):
        count += 1
    
    grSheet = wb.get_sheet_by_name("Goodreads")
    newRow = grSheet.max_row + 1
    grSheet["A{}".format(newRow)] = "=DATE({})".format(datetime.date.today().strftime("%Y,%m,%d"))
    
    grSheet["B{}".format(newRow)] = count
    
    return wb
