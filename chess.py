# Component of trackr.py - saves data from Chess.com
# Requires a username in personal.data

import json
import requests

from getDate import get_date
import personal

def update_Chess(cur):
    # Pull and load JSON data
    chessUrl = "https://api.chess.com/pub/player/{}/stats".format(personal.data["chessUsername"])
    chessResponse = requests.get(chessUrl)
    chessResponse.raise_for_status()
    chessData = json.loads(chessResponse.text)
    
    # Select most recent entry
    cur.execute("SELECT Date FROM chess ORDER BY Date DESC LIMIT 1")
    last_entry = cur.fetchone()
    
    # If last entry is not today, add new data. Else skip.
    today = get_date()
    if today != last_entry[0]:
        sql = ''' INSERT INTO chess(Date, Daily, Daily960, Rapid, Bullet, Blitz) VALUES (?,?,?,?,?,?)'''
        new_entry = [today, chessData["chess_daily"]["last"]["rating"], 0, chessData["chess_rapid"]["last"]["rating"], chessData["chess_bullet"]["last"]["rating"], chessData["chess_blitz"]["last"]["rating"]]
        cur.execute(sql, new_entry[0:6])
        print("New data added to Chess.")
    else:
        print("Chess was already updated today.")
    
    return cur
    
