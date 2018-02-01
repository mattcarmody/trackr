# Component of trackr.py - saves data from Chess.com
# Requires a username in personal.data

import datetime
import json
import requests

import personal

def update_Chess(wb):
    chessUrl = "https://api.chess.com/pub/player/" + personal.data["chessUsername"] + "/stats"
    chessResponse = requests.get(chessUrl)
    chessResponse.raise_for_status()
    chessData = json.loads(chessResponse.text)
    
    chessSheet = wb.get_sheet_by_name("Chess")
    newRow = chessSheet.max_row + 1
    chessSheet["A" + str(newRow)] = "=DATE(" + datetime.date.today().strftime("%Y,%m,%d") + ")"
    
    chessSheet["B" + str(newRow)] = chessData["chess_daily"]["last"]["rating"]
    chessSheet["C" + str(newRow)] = chessData["chess960_daily"]["last"]["rating"]
    chessSheet["D" + str(newRow)] = chessData["chess_rapid"]["last"]["rating"]
    chessSheet["E" + str(newRow)] = chessData["chess_bullet"]["last"]["rating"]
    chessSheet["F" + str(newRow)] = chessData["chess_blitz"]["last"]["rating"]
    
    return wb
    
