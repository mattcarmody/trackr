#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import bs4
import datetime
import json
import openpyxl
import requests

def update_Duolingo(wb):
    
    duoUrl = "https://www.duolingo.com/users/{USERNAME}"
    duoResponse = requests.get(duoUrl)
    duoResponse.raise_for_status()
    duoData = json.loads(duoResponse.text)
    
    duoSheet = wb.get_sheet_by_name("Duolingo")
    newRow = duoSheet.max_row + 1
    duoSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")

    for i in range(len(duoData["languages"])):
        duoSheet[str(openpyxl.utils.get_column_letter(i+2)) + str(newRow)] = duoData["languages"][i]["points"]
        
    return wb
    
def update_Codewars(wb):
    cwUrl = "https://www.codewars.com/api/v1/users/{USERNAME}"
    cwResponse = requests.get(cwUrl, auth=("?access_key", "{ACCESS_KEY}"))
    cwResponse.raise_for_status()
    cwData = json.loads(cwResponse.text)
    
    cwSheet = wb.get_sheet_by_name("Codewars")
    newRow = cwSheet.max_row + 1
    cwSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")
    
    cwSheet["B" + str(newRow)] = cwData["honor"]
    
    return wb
    
def update_Chess(wb):
    chessUrl = "https://api.chess.com/pub/player/{USERNAME}/stats"
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
    
    bsUrl = "https://www.goodreads.com/review/list/{USER_ID}?shelf={SHELF}"
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
    wb.save('trackr.xlsx')
    
main()
