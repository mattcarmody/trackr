#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import bs4
import datetime
import json
import openpyxl
import requests

from hackerRank import update_HackerRank
from duolingo import update_Duolingo

import personal
    
def update_Codewars(wb):
    cwUrl = "https://www.codewars.com/api/v1/users/" + personal.data["cwUsername"]
    cwResponse = requests.get(cwUrl, auth=("?access_key", personal.data["cwAccessKey"]))
    cwResponse.raise_for_status()
    cwData = json.loads(cwResponse.text)
    
    cwSheet = wb.get_sheet_by_name("Codewars")
    newRow = cwSheet.max_row + 1
    cwSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")
    
    cwSheet["B" + str(newRow)] = cwData["honor"]
    
    return wb
    
def update_Chess(wb):
    chessUrl = "https://api.chess.com/pub/player/" + personal.data["chessUsername"] + "/stats"
    chessResponse = requests.get(chessUrl)
    chessResponse.raise_for_status()
    chessData = json.loads(chessResponse.text)
    
    chessSheet = wb.get_sheet_by_name("Chess")
    newRow = chessSheet.max_row + 1
    chessSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")
    
    chessSheet["B" + str(newRow)] = chessData["chess_daily"]["last"]["rating"]
    chessSheet["C" + str(newRow)] = chessData["chess960_daily"]["last"]["rating"]
    chessSheet["D" + str(newRow)] = chessData["chess_rapid"]["last"]["rating"]
    chessSheet["E" + str(newRow)] = chessData["chess_bullet"]["last"]["rating"]
    chessSheet["F" + str(newRow)] = chessData["chess_blitz"]["last"]["rating"]
    
    return wb
    
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
    #wb = update_Codewars(wb)
    #wb = update_Chess(wb)
    #wb = update_Goodreads(wb)
    #wb = update_HackerRank(wb)
    wb.save('trackr.xlsx')
    
main()
