#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import bs4
import datetime
import json
import openpyxl
import requests

from hackerRank import update_HackerRank
from duolingo import update_Duolingo
from codewars import update_Codewars
from chess import update_Chess

import personal
    
def update_Goodreads(wb):
    
    bsUrl = "https://www.goodreads.com/review/list/" + personal.data["grUserID"] + "?shelf=" + personal.data["grShelf"]
    res = requests.get(bsUrl)
    res.raise_for_status()
    bsSoup = bs4.BeautifulSoup(res.text, "lxml")
    booksTable = bsSoup.find("table", {"id" : "books"})
    count = -1
    for row in booksTable.findAll("tr"):
        count += 1
    
    grSheet = wb.get_sheet_by_name("Goodreads")
    newRow = grSheet.max_row + 1
    grSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")
    
    grSheet["B" + str(newRow)] = count
    
    return wb

def main():
    wb = openpyxl.load_workbook('trackr.xlsx')      
    wb = update_Duolingo(wb)
    wb = update_Codewars(wb)
    wb = update_Chess(wb)
    wb = update_Goodreads(wb)
    wb = update_HackerRank(wb)
    wb.save('trackr.xlsx')
    
main()
