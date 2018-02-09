#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

### SWITCHING FROM XLSX TO SQLITE3 DB ###

#import openpyxl
import sqlite3

from hackerRank import update_HackerRank
from duolingo import update_Duolingo
from codewars import update_Codewars
from chess import update_Chess
from goodreads import update_Goodreads
import pullFromEmail

import personal

def main():
    conn = sqlite3.connect("trackr.db")
    with conn:
        #wb = openpyxl.load_workbook(personal.data["xlsxTrackr"])      
        #try:
        cur = conn.cursor()
        cur = update_Duolingo(cur)
        '''except:
            print("Duolingo failed...")
        try:
            conn = update_Codewars(wb)
        except:
            print("Codewars failed...")
        try:
            wb = update_Chess(wb)
        except:
            print("Chess failed...")
        try:
            wb = update_Goodreads(wb)
        except:
            print("Goodreads failed...")
        try:
            wb = update_HackerRank(wb)
        except:
            print("HackerRank failed...")
        try:
            wb = pullFromEmail.update_Email(wb)
        except:
            print("Email update failed...")
        '''
    #conn.close()
    #wb.save(personal.data["xlsxTrackr"])
    
if __name__ == "__main__":
    main()
