#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent and provide the
# manager part of myself with tracking of the worker part of myself.

import datetime
import importlib
import logging
logging.basicConfig(filename='trackr_log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
import sqlite3
import sys
import traceback

# Import trackr update modules. (Add new in both modules and functions)
modules = ["duolingo", "codewars", "chess", "goodreads", "my_email", "track_warmup"]
gbl = globals()
for module in modules:
    gbl[module] = importlib.import_module(module)    
functions = [duolingo.update_duolingo, codewars.update_codewars, chess.update_chess, goodreads.update_goodreads, my_email.update_my_email, track_warmup.update_track_warmup]

import visuals_body
import visuals_duolingo
import visuals_deepwork

import personal

# Bifort 1: Jan 1 - Jan 28. Jan 1 is a Monday
BIFORT_START = 1
REVIEW_DOW = 6

def main():
    logging.debug("Start main.")
    conn = sqlite3.connect("trackr.db")
    with conn:     
        cur = conn.cursor()
        
        # Update functions
        for f in functions:
            try:
                cur = f(cur)
            except:
                with open("trackr_log.txt", "a") as error_file:
                    error_file.write(traceback.format_exc())
                print(str(f) + " failed...")
        
        # Visualizations
        try:
            today = datetime.date.today()
            day_of_year = datetime.date.today().timetuple().tm_yday
                
            # Bifortly (every 4 Sundays)
            if today.weekday() == REVIEW_DOW and ((day_of_year - BIFORT_START + 1) // 7) % 4 == 0:
                visuals_duolingo.duolingo_bifortly_visuals(cur)
                
            # Weekly
            if today.weekday() == REVIEW_DOW:
                pass
            
            # Each call
            if True:
                visuals_duolingo.duolingo_weekly_visuals(cur)
                visuals_body.body_week_visuals(cur)
                visuals_deepwork.deepwork_week_visuals(cur)
        except:
            with open("trackr_log.txt", "a") as error_file:
                error_file.write(traceback.format_exc())
            print("Visualizations failed...")
        
    logging.debug("Finish main.")
        
if __name__ == "__main__":
    main()
    
