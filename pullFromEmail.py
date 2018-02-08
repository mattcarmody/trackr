#!/usr/bin/python3
# pullFromEmail.py - Adds activities from my email inbox to spreadsheet
# I dicatate these emails to Siri, they follow a predictable format of:
# keyword num keyword num keyword num ...
# Requires information stored in personal.py

import datetime
import email
import imapclient
import pyzmail

import personal

TRACKR_EMAIL_ADDRESS = personal.data["trackrEmail"]
SECRET_PASSWORD = personal.data["trackrEmailPassword"]
PERSONAL_EMAIL_ADDRESS = personal.data["Email"]
FOLDER = 'INBOX'
METRIC_COLUMN_DICT = personal.bodyDict

# Changes "one" or "1" to 1, Borrowed from stack overflow with minor changes
def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", 
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", 
            "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
            "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", 
                "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand"]

        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: {}".format(word))
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    return result + current

def update_Email(wb):    
    bodySheet = wb.get_sheet_by_name("Body")    
    
    # Connect to dedicated email account and fetch relevant, unopened emails
    imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imapObj.login(TRACKR_EMAIL_ADDRESS, SECRET_PASSWORD)
    imapObj.select_folder(FOLDER, readonly=False)
    UIDs = imapObj.search(['FROM', PERSONAL_EMAIL_ADDRESS, 'UNSEEN'])
    rawMessages = imapObj.fetch(UIDs, ['BODY[]'])
    
    for i in range(len(UIDs)): # For each email
        message = pyzmail.PyzMessage.factory(rawMessages[UIDs[i]][b'BODY[]'])    
        # Verify that it is a text body as expected, not HTML
        if message.text_part != None:
            body = message.text_part.get_payload().decode(message.text_part.charset)
        elif message.html_part != None:
            print("This is an HTML message...")
            continue
        else:
            print("No text or html parts. Maybe no message?")
            continue
        
        # Trim footer and convert any numbers to integers
        body = body.replace("Sent from my iPhone", "")
        words = body.split()
        for i, word in enumerate(words):
            try:
                words[i] = text2int(word)
            except:
                try:
                    words[i] = int(word)
                except:
                    pass
        
        # Combine multi-word keywords (string items alongside one another)
        for i in range(len(words)-2, -1, -1):
            if type(words[i]) == str and type(words[i+1]) == str:
                words[i] = "{} {}".format(words[i], words[i+1])
                del words[i+1]   

        # Get row number by date of the email
        date = message['Date']
        pDate = datetime.datetime.strptime(date , '%a, %d %b %Y %X %z').strftime('=DATE(%Y,%-m,%-d)')
        max_row = bodySheet.max_row
        row = max_row - 2 # placeholder in noticeable location in xlsx
        for i in range(1, max_row+1):
            if bodySheet["A{}".format(i)].value == pDate:
                row = i
                break
        
        # Update xlsx for each keyword/number pair
        for i in range(0, len(words), 2):
            # Get column letter
            if type(words[i]) != str:
                print("Oh no! I was expecting a str, not {}".format(type(words[i])))
                break
            col = "N" #Default to Uncategorized column
            for key in METRIC_COLUMN_DICT:
                if key in words[i].lower():
                    col = METRIC_COLUMN_DICT[key]
                    
            # Update cell value
            bodySheet["{}{}".format(col, row)].value += words[i+1]
            print("Adding {} to {}{}".format(words[i+1], col, row))
            
    print("Update from email complete.")
    imapObj.logout()
    return wb

