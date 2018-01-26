# Component of trackr.py - saves data from Codewars.com
# Requires a username and accesskey in personal.data

import datetime
import json
import requests

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
