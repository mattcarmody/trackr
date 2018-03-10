#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import datetime
import logging
logging.basicConfig(filename='trackr_log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
import sqlite3
import sys
import traceback

from hackerRank import update_HackerRank
from duolingo import update_Duolingo
from codewars import update_Codewars
from chess import update_Chess
from goodreads import update_Goodreads
import pullFromEmail
from trackWarmUp import update_warmup

import bodyVisuals
import duolingoVisuals
import deepWorkVisuals

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
            cur = update_Duolingo(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Duolingo failed...")
        try:
            cur = update_Codewars(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Codewars failed...")
        try:
            cur = update_Chess(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Chess failed...")
        try:
            cur = update_Goodreads(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Goodreads failed...")
        #try:
        #    cur = update_HackerRank(cur)
        #except:
            #with open("trackr_log.txt", "a") as error_file:
                #error_file.write(traceback.format_exc())    
            #print("HackerRank failed...")
        try:
            cur = pullFromEmail.update_email(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Email update failed...")
        try:
            cur = update_warmup(cur)
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
                #duolingoVisuals.duolingo_weekly_visuals(cur)
                bodyVisuals.body_week_visuals(cur)
                deepWorkVisuals.deepWork_week_visuals(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Visualizations failed...")
    logging.debug("Finish main.")
        
if __name__ == "__main__":
    main()
    
