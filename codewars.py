# Component of trackr.py - saves data from Codewars.com
# Requires a username and accesskey in personal.data

import json
import requests

from getDate import get_date
import personal

def update_Codewars(wb):
    cwUrl = "https://www.codewars.com/api/v1/users/{}".format(personal.data["cwUsername"])
    cwResponse = requests.get(cwUrl, auth=("?access_key", personal.data["cwAccessKey"]))
    cwResponse.raise_for_status()
    cwData = json.loads(cwResponse.text)
    
    cwSheet = wb.get_sheet_by_name("Codewars")
    newRow = cwSheet.max_row + 1
    
    today = get_date()
    if not cwSheet["A{}".format(newRow-1)].value == today:
        cwSheet["A{}".format(newRow)] = today
        cwSheet["B{}".format(newRow)] = cwData["honor"]
        cwSheet["C{}".format(newRow)] = cwData["ranks"]["overall"]["score"]
        cwSheet["D{}".format(newRow)] = cwData["codeChallenges"]["totalCompleted"]
        print("Updated codewars.")
    else:
        print("Codewars already has data for today.")
    
    return wb
