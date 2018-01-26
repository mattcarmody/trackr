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
    wb = openpyxl.load_workbook('trackr.xlsx')      
    wb = update_Duolingo(wb)
    wb = update_Codewars(wb)
    wb = update_Chess(wb)
    wb = update_Goodreads(wb)
    wb = update_HackerRank(wb)
    wb.save('trackr.xlsx')
    
main()
