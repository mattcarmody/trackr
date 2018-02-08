# Component of trackr.py - saves data from Goodreads.com
# Requires a user ID and shelf in personal.data

import bs4
import requests

from getDate import get_date
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
    
    today = get_date()
    if not grSheet["A{}".format(newRow-1)].value == today:
        grSheet["A{}".format(newRow)] = today
        grSheet["B{}".format(newRow)] = count
        print("Updated Goodreads.")
    else:
        print("Goodreads has already been updated today.")
    
    return wb
