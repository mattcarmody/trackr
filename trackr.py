#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import datetime
import sqlite3
import sys

from hackerRank import update_HackerRank
from duolingo import update_Duolingo
from codewars import update_Codewars
from chess import update_Chess
from goodreads import update_Goodreads
import pullFromEmail
import duolingoVisuals

import personal

# bifort 1: Jan 1 - Jan 28 (because Jan 1 is a Monday)
BIFORT_START = 1
REVIEW_DOW = 0

def main():
    conn = sqlite3.connect("trackr.db")
    with conn:     
        cur = conn.cursor()
        
        try:
            cur = update_Duolingo(cur)
        except:
            print("Duolingo failed...")
        try:
            cur = update_Codewars(cur)
        except:
            print("Codewars failed...")
        try:
            cur = update_Chess(cur)
        except:
            print("Chess failed...")
        try:
            cur = update_Goodreads(cur)
        except:
            print("Goodreads failed...")
        try:
            cur = update_HackerRank(cur)
        except:
            print("HackerRank failed...")
        try:
            cur = pullFromEmail.update_Email(cur)
        except:
            print("Email update failed...")
        
        if len(sys.argv) > 1:
            today = datetime.date.today()
            # Annual
            if today.day == 1 and today.month == 1:
                # Annual stuff here
                pass
                
            # Quarterly
            if today.month % 3 == 0 and today.day == 1:
                # Quarterly stuff here
                pass
            
            #day_of_year = datetime.date.today().timetuple().tm_yday
            day_of_year = 29
            print(day_of_year)
                
            # Bifortly
            if today.weekday() == REVIEW_DOW and ((day_of_year - BIFORT_START) // 7) % 4 == 0:
                duolingoVisuals.duolingo_bifortly_visuals(cur)
                
            # Weekly
            if today.weekday() == REVIEW_DOW:
                duolingoVisuals.duolingo_weekly_visuals(cur)
    
if __name__ == "__main__":
    main()
    
