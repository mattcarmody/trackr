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

# Update functions to be called each runtime
functions = [duolingo.update_duolingo, codewars.update_codewars, chess.update_chess, goodreads.update_goodreads, my_email.update_my_email, track_warmup.update_track_warmup]

import visuals_body
import visuals_duolingo
import visuals_deepwork

import personal

# A bifort is a unit of time equal to 28 days starting on Monday
# Bifort 1 starts at 1 because Jan 1 is a Monday
BIFORT_START = 1
REVIEW_DOW = 6

def main():
	logging.debug("Start main.")
	conn = sqlite3.connect("trackr.db")
	with conn:     
		cur = conn.cursor()
		# Update function calls
		for f in functions:
			try:
				cur = f(cur)
			except:
				with open("trackr_log.txt", "a") as error_file:
					error_file.write(traceback.format_exc())
				print(str(f) + " failed...")
		# Visualization function calls
		try:
			today = datetime.date.today()
			day_of_year = datetime.date.today().timetuple().tm_yday 
			# Bifortly (every 4th Sunday)
			if today.weekday() == REVIEW_DOW and ((day_of_year - BIFORT_START + 1) // 7) % 4 == 0:
				visuals_duolingo.duolingo_bifortly_visuals(cur)
			# Weekly
			if today.weekday() == REVIEW_DOW:
				visuals_duolingo.duolingo_weekly_visuals(cur)
			# Each call
			if True:
				'''try:
					visuals_body.body_week_visuals(cur)
				except:
					print("Body visuals failed")
					logging.critical("Body visuals failed!")'''
				try:
					visuals_deepwork.deepwork_week_visuals(cur)
				except:
					print("Deep work visuals failed")
					logging.critical("Deep work visuals failed!")
		except:
			with open("trackr_log.txt", "a") as error_file:
				error_file.write(traceback.format_exc())
			print("Visualizations failed...")
			logging.critical("Visualizations failed!")
	logging.debug("Finish main.")
		
if __name__ == "__main__":
	main()
	
