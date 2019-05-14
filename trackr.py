#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent and provide the
# manager part of myself with tracking of the worker part of myself.

import datetime
import logging
import sqlite3
import sys
import traceback

logging.basicConfig(filename='trackr_log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

import chess
import codewars
import duolingo
import goodreads
import my_email
import track_warmup

import visuals_body
import visuals_duolingo
import visuals_deepwork

import personal

# A bifort is a unit of time equal to 28 days starting on Monday
# Bifort 1 starts at 1 because Jan 1 is a Monday
BIFORT_START = 1
REVIEW_DOW = 6

def call_functions(cur, function_list):
	for f in function_list:
		try:
			f(cur)
		except:
			with open("trackr_log.txt", "a") as error_file:
				error_file.write(traceback.format_exc())
			print(str(f) + " failed...")
			
def call_track_functions(cur):
	call_functions(cur, track_functions)

def call_viz_functions(cur):
	today = datetime.date.today()
	day_of_year = datetime.date.today().timetuple().tm_yday 
	# Bifortly (every 4th Sunday)
	if today.weekday() == REVIEW_DOW and ((day_of_year - BIFORT_START + 1) // 7) % 4 == 0:
		call_functions(cur, bifortly_viz_functions)
	# Weekly
	if today.weekday() == REVIEW_DOW:
		call_functions(cur, weekly_viz_functions)
	# Daily
	if True:
		call_functions(cur, daily_viz_functions)

track_functions = [
	duolingo.update_duolingo, 
	codewars.update_codewars, 
	chess.update_chess, 
	goodreads.check_goodreads, 
	my_email.update_my_email, 
	]
bifortly_viz_functions = [
	visuals_duolingo.duolingo_bifortly_visuals,
	]
weekly_viz_functions = [
	visuals_duolingo.duolingo_weekly_visuals,
	]
daily_viz_functions = [
	visuals_body.body_week_visuals,
	visuals_deepwork.deepwork_week_visuals,
	]

def main():
	logging.debug("\n\n\nStart main.")
	conn = sqlite3.connect("trackr.db")
	with conn:     
		cur = conn.cursor()
		call_track_functions(cur)
		call_viz_functions(cur)
	logging.debug("Finish main.")
		
if __name__ == "__main__":
	main()
	
