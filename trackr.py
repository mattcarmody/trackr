#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

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
        
if __name__ == "__main__":
    main()
