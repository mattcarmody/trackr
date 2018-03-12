#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent and provide
# manager part of myself with tracking of the worker part of myself.

import datetime
import logging
logging.basicConfig(filename='trackr_log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
import sqlite3
import sys
import traceback

from hackerrank import update_hackerrank
from duolingo import update_duolingo
from codewars import update_codewars
from chess import update_chess
from goodreads import update_goodreads
from my_email import update_my_email
from track_warmup import update_track_warmup

import visuals_Body
import visuals_Duolingo
import visuals_Deep_Work

import personal

# Bifort 1: Jan 1 - Jan 28. Jan 1 is a Monday
BIFORT_START = 1
REVIEW_DOW = 6

def main():
    logging.debug("Start main.")
    conn = sqlite3.connect("trackr.db")
    with conn:     
        cur = conn.cursor()
        
        try:
            cur = update_duolingo(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Duolingo failed...")
        try:
            cur = update_codewars(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Codewars failed...")
        try:
            cur = update_chess(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Chess failed...")
        try:
            cur = update_goodreads(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Goodreads failed...")
        #try:
        #    cur = update_hackerrank(cur)
        #except:
            #with open("trackr_log.txt", "a") as error_file:
                #error_file.write(traceback.format_exc())    
            #print("HackerRank failed...")
        try:
            cur = update_my_email(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Email update failed...")
        try:
            cur = update_track_warmup(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("There was a problem updating warmup.")
        try:
            today = datetime.date.today()
            day_of_year = datetime.date.today().timetuple().tm_yday
                
            # Bifortly
            if today.weekday() == REVIEW_DOW and ((day_of_year - BIFORT_START + 1) // 7) % 4 == 0:
                duolingoVisuals.duolingo_bifortly_visuals(cur)
                
            # Weekly
            #if today.weekday() == REVIEW_DOW:
            
            # Daily
            if True:
                #visuals_Duolingo.duolingo_weekly_visuals(cur)
                visuals_Body.body_week_visuals(cur)
                visuals_Deep_Work.deepWork_week_visuals(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Visualizations failed...")
    logging.debug("Finish main.")
        
if __name__ == "__main__":
    main()
    
