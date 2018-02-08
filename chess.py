# Component of trackr.py - saves data from Chess.com
# Requires a username in personal.data

import json
import requests

from getDate import get_date
import personal

def update_Chess(wb):
    chessUrl = "https://api.chess.com/pub/player/{}/stats".format(personal.data["chessUsername"])
    chessResponse = requests.get(chessUrl)
    chessResponse.raise_for_status()
    chessData = json.loads(chessResponse.text)
    
    chessSheet = wb.get_sheet_by_name("Chess")
    newRow = chessSheet.max_row + 1
    
    today = get_date()
    if not chessSheet["A{}".format(newRow-1)].value == today:
        chessSheet["A{}".format(newRow)] = today
        chessSheet["B{}".format(newRow)] = chessData["chess_daily"]["last"]["rating"]
        chessSheet["C{}".format(newRow)] = chessData["chess960_daily"]["last"]["rating"]
        chessSheet["D{}".format(newRow)] = chessData["chess_rapid"]["last"]["rating"]
        chessSheet["E{}".format(newRow)] = chessData["chess_bullet"]["last"]["rating"]
        chessSheet["F{}".format(newRow)] = chessData["chess_blitz"]["last"]["rating"]
        print("Updated chess ratings.")
    else:
        print("Chess already has ratings for today.")
    
    return wb
    
