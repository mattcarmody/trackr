#!/usr/bin/python3
# trackr.py - Automate record keeping for sites I frequent.

import openpyxl

from hackerRank import update_HackerRank
from duolingo import update_Duolingo
from codewars import update_Codewars
from chess import update_Chess
from goodreads import update_Goodreads

import personal

def main():
    wb = openpyxl.load_workbook(personal.data["xlsxTrackr"])      
    try:
        wb = update_Duolingo(wb)
    except:
        print("Duolingo failed...")
    try:
        wb = update_Codewars(wb)
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
    wb.save(personal.data["xlsxTrackr"])
    
main()
