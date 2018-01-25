#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import bs4
import datetime
import json
import openpyxl
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def update_HackerRank(wb):
    url = "https://www.hackerrank.com/{USERNAME}"

    browser = webdriver.Firefox()
    browser.get(url)
    loginElem = browser.find_element_by_class_name("login").click()

    username = browser.find_element_by_name("login")
    username.send_keys("{EMAIL}")

    password = browser.find_element_by_name("password")
    password.send_keys("{PASSWORD}")
    password.send_keys(Keys.RETURN)

    hackosUrl = "https://www.hackerrank.com/{USERNAME}/hackos"
    browser.get(hackosUrl)
    browser.refresh()

    innerHTML = browser.execute_script("return document.body.innerHTML")
    bsSoup = bs4.BeautifulSoup(innerHTML, "lxml")
    h3 = bsSoup.find("h3")

    hackosRegex = re.compile(r"Total Hackos: (\d*)")
    mo = hackosRegex.search(h3.text)
    hackos = int(mo.group(1))

    hrSheet = wb.get_sheet_by_name("HackerRank")
    newRow = hrSheet.max_row + 1
    hrSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")
    hrSheet["B" + str(newRow)] = hackos
    
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
