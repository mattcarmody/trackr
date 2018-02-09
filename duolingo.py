# Component of trackr.py - saves data from Duolingo.com
# Requires a username in personal.data

import json
import requests
import sqlite3

from getDate import get_date
import personal

def update_Duolingo(cur):    
    # Pull and load JSON data
    duoUrl = "https://www.duolingo.com/users/{}".format(personal.data["duoUsername"])
    duoResponse = requests.get(duoUrl)
    duoResponse.raise_for_status()
    duoData = json.loads(duoResponse.text)
    
    # Select most recent entry
    cur.execute("SELECT Date FROM duolingo ORDER BY Date DESC LIMIT 1")
    last_entry = cur.fetchone()
    
    # If last entry is not today, add new data. Else skip.
    today = get_date()
    if today != last_entry[0]:
        sql = ''' INSERT INTO duolingo(Date, Greek, Esperanto, Vietnamese, Italian, Welsh, Irish, Czech, Spanish, Chinese, Russian, Portuguese, Norwegian, Turkish, Romanian, Polish, Dutch, French, German, HighValyrian, Korean, Danish, Hungarian, Japanese, Hebrew, Swahili, Swedish, Ukrainian) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        new_entry = [today]
        for i in range(len(duoData["languages"])):
            new_entry.append(duoData["languages"][i]["points"])
        cur.execute(sql, new_entry[0:28])
        print("New data added to Duolingo.")
    else:
        print("Duolingo was already updated today.")
    
    '''    
    duoSheet = wb.get_sheet_by_name("Duolingo")
    newRow = duoSheet.max_row + 1
    
    if not duoSheet["A{}".format(newRow-1)].value == today:
        duoSheet["A{}".format(newRow)] = today
        for i in range(len(duoData["languages"])):
            duoSheet["{}{}".format(openpyxl.utils.get_column_letter(i+2), newRow)] = duoData["languages"][i]["points"]
        print("Updated Duolingo.")
    else:
        print("Duolingo was already updated today.")
    '''
    return cur
