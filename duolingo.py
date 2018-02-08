# Component of trackr.py - saves data from Duolingo.com
# Requires a username in personal.data

import json
import openpyxl
import requests

from getDate import get_date
import personal

def update_Duolingo(wb):
    
    duoUrl = "https://www.duolingo.com/users/{}".format(personal.data["duoUsername"])
    duoResponse = requests.get(duoUrl)
    duoResponse.raise_for_status()
    duoData = json.loads(duoResponse.text)
    
    duoSheet = wb.get_sheet_by_name("Duolingo")
    newRow = duoSheet.max_row + 1
    
    today = get_date()
    if not duoSheet["A{}".format(newRow-1)].value == today:
        duoSheet["A{}".format(newRow)] = today
        for i in range(len(duoData["languages"])):
            duoSheet["{}{}".format(openpyxl.utils.get_column_letter(i+2), newRow)] = duoData["languages"][i]["points"]
        print("Updated Duolingo.")
    else:
        print("Duolingo was already updated today.")
        
    return wb
