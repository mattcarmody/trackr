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
METRIC_COLUMN_DICT = personal.emailDict
DEF_COL = 10
DEF_COL_NAME = "Uncategorized"

# Changes "one" or "1" to 1, Borrowed from stack overflow with minor changes
def text_to_int(num_text, num_words={}):
    if not num_words:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", 
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", 
            "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
            "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", 
                "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand"]

        for i, word in enumerate(units):
            num_words[word] = (1, i)
        for i, word in enumerate(tens):
            num_words[word] = (1, i * 10)
        for i, word in enumerate(scales):
            num_words[word] = (10 ** (i * 3 or 2), 0)

    current = result = 0
    for word in num_text.split():
        if word not in num_words:
            raise Exception("Illegal word: {}".format(word))
        scale, increment = num_words[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    return result + current

def update_email(cur):    
    # Connect to dedicated email account and fetch relevant, unopened emails
    imap_obj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imap_obj.login(TRACKR_EMAIL_ADDRESS, SECRET_PASSWORD)
    imap_obj.select_folder(FOLDER, readonly=False)
    UIDs = imap_obj.search(['FROM', PERSONAL_EMAIL_ADDRESS, 'UNSEEN'])
    raw_messages = imap_obj.fetch(UIDs, ['BODY[]'])
    
    for i in range(len(UIDs)): # For each email
        message = pyzmail.PyzMessage.factory(raw_messages[UIDs[i]][b'BODY[]'])    
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
                words[i] = text_to_int(word)
            except:
                try:
                    words[i] = int(word)
                except:
                    pass
        
        # Combine multi-word keywords (string items alongside one another)
        # Work back from end to prevent skips and handle 3+ words
        for i in range(len(words)-2, -1, -1):
            if type(words[i]) == str and type(words[i+1]) == str:
                words[i] = "{} {}".format(words[i], words[i+1])
                del words[i+1]   

        # Choose db based on subject body/work
        if "body" in message.get_subject().lower():
            table = "body"
        elif "work" in message.get_subject().lower():
            table = "deepWork"
        else:
            print("I don't know which table to use for this email subject: {} (so I'm skipping it)".format(message.get_subject()))
            continue
            
        # Call relevant db row for the email date
        date = message['Date']
        pars_date = datetime.datetime.strptime(date, '%a, %d %b %Y %X %z').strftime('%Y-%m-%d')
        cur.execute('SELECT * FROM \"{}\" WHERE Date = \"{}\"'.format(table, pars_date))
        rel_entry = cur.fetchone()
        
        # Update relevant value for each keyword/number pair
        for i in range(0, len(words), 2):
            if type(words[i]) != str:
                print("Oh no! I was expecting a str, not {}".format(type(words[i])))
                break
            for key in METRIC_COLUMN_DICT:
                col = DEF_COL
                col_name = DEF_COL_NAME
                if key in words[i].lower():
                    col = METRIC_COLUMN_DICT[key][0]
                    col_name = METRIC_COLUMN_DICT[key][1]
                    break
                   
            new_value = rel_entry[col] + words[i+1]
            cur.execute('UPDATE {} SET {} = {} WHERE Date = \"{}\"'.format(table, col_name, new_value, pars_date))
            print("Adding {} to {}'s {} on {}.".format(words[i+1], table, col_name, pars_date))

    print("Update from email complete.")
    imap_obj.logout()
    return cur
    
