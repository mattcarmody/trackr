# Component of trackr.py - saves data from Chess.com
# Requires a username in personal.data

import json
import requests

import date_related
import personal

def scrape_chess():
	chessUrl = "https://api.chess.com/pub/player/{}/stats".format(personal.data["chessUsername"])
	chessResponse = requests.get(chessUrl)
	chessResponse.raise_for_status()
	return json.loads(chessResponse.text)
	
def track_chess(cur):
	last_entry_date = date_related.get_date_of_last_entry(cur, "chess")
	today = date_related.get_date()

	if today != last_entry_date[0]:
		chessData = scrape_chess()
		sql = ''' INSERT INTO chess(Date, Daily, Daily960, Rapid, Bullet, Blitz) VALUES (?,?,?,?,?,?)'''
		new_entry = [today, chessData["chess_daily"]["last"]["rating"], 0, chessData["chess_rapid"]["last"]["rating"], chessData["chess_bullet"]["last"]["rating"], chessData["chess_blitz"]["last"]["rating"]]
		cur.execute(sql, new_entry[0:6])
		print("New data added to Chess.")
	else:
		print("Chess was already updated today.")
	
