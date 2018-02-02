# Component of trackr.py - saves data from Duolingo.com
# Requires a username in personal.data

import datetime
import json
import openpyxl
import requests

import personal

def update_Duolingo(wb):
    
    duoUrl = "https://www.duolingo.com/users/{}".format(personal.data["duoUsername"])
    duoResponse = requests.get(duoUrl)
    duoResponse.raise_for_status()
    duoData = json.loads(duoResponse.text)
    
    duoSheet = wb.get_sheet_by_name("Duolingo")
    newRow = duoSheet.max_row + 1
    duoSheet["A{}".format(newRow)] = "=DATE({})".format(datetime.date.today().strftime("%Y,%m,%d"))

    for i in range(len(duoData["languages"])):
        duoSheet["{}{}".format(openpyxl.utils.get_column_letter(i+2), newRow)] = duoData["languages"][i]["points"]
        
    return wb
