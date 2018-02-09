# Component of trackr.py - saves data from Codewars.com
# Requires a username and accesskey in personal.data

import json
import requests

from getDate import get_date
import personal

def update_Codewars(cur):
    # Pull and load JSON data
    cwUrl = "https://www.codewars.com/api/v1/users/{}".format(personal.data["cwUsername"])
    cwResponse = requests.get(cwUrl, auth=("?access_key", personal.data["cwAccessKey"]))
    cwResponse.raise_for_status()
    cwData = json.loads(cwResponse.text)
    
    # Select most recent entry
    cur.execute("SELECT Date FROM codewars ORDER BY Date DESC LIMIT 1")
    last_entry = cur.fetchone()
    
    # If last entry is not today, add new data. Else skip.
    today = get_date()
    if today != last_entry[0]:
        sql = ''' INSERT INTO codewars(Date, Honor, Points, Challenges) VALUES (?,?,?,?)'''
        new_entry = [today, cwData["honor"], cwData["ranks"]["overall"]["score"], cwData["codeChallenges"]["totalCompleted"]]
        cur.execute(sql, new_entry[0:4])
        print("New data added to Codewars.")
    else:
        print("Codewars was already updated today.")
    
    return cur
    
