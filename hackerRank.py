# Component of trackr.py - saves data from HackerRank.com
# Requires username and password in personal.data

import bs4
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from getDate import get_date
import personal

def update_HackerRank(cur):
    today = get_date()
    
    # Navigate through login with Selenium
    url = "https://www.hackerrank.com/{}".format(personal.data["hrUsername"])

    browser = webdriver.Firefox()
    browser.get(url)
    loginElem = browser.find_element_by_class_name("login").click()

    username = browser.find_element_by_name("login")
    username.send_keys(personal.data["hrUsername"])

    password = browser.find_element_by_name("password")
    password.send_keys(personal.data["hrPassword"])
    password.send_keys(Keys.RETURN)

    #Estimate number of pages in HackerRank table
    cur.execute("SELECT Count(*) FROM hackerRankItems")
    items = cur.fetchone()
    maxPage = items[0] // 10 + 2
    
    # Navigate through pages of history
    data = []
    for page in range(1, maxPage):
        hackosUrl = "https://www.hackerrank.com/{}/hackos/page/{}".format(personal.data["hrUsername"], page)
        browser.get(hackosUrl)
        
        # Often has a 404 error, but refreshing helps
        count = 0
        while count < 5:
            innerHTML = browser.execute_script("return document.body.innerHTML")
            bsSoup = bs4.BeautifulSoup(innerHTML, "lxml")
            try:
                h3 = bsSoup.find("h3")
                if "Hackos" in h3.text:
                    break
            except:
                count += 1
                browser.refresh()
        
        # Close if it is still on 404
        if not h3:
            browser.quit()
            print("HackerRank - 404.")
            return cur
        
        # Extract Total Hackos count from first page
        if page == 1:
            hackosRegex = re.compile(r"Total Hackos: (\d*)")
            mo = hackosRegex.search(h3.text)
            hackos = int(mo.group(1))
        
        # Extract table data line by line
        table = bsSoup.findAll("div", {"class":"hacko-transaction-list-view"})
        try:
            for row in table:
                temp = []
                for col in row.findAll("p"):
                    temp.append(col.text)
                data.append(temp)
        except:
            pass
        
    # Renumber IDs (reverse direction)
    data = data[::-1]
    for i in range(len(data)):
        data[i][0] = i+1
    
    
    # Add to hackerRankItems table
    cur.execute("SELECT * FROM hackerRankItems ORDER BY SlNumber")
    all_entries = cur.fetchall()
    
    selectAdd = 0
    diff = len(data) - len(all_entries)
    
    if diff == 0:
        print("No new line items in HackerRank.")
    for i in range(diff):
        index = i + len(all_entries)
        sql = '''INSERT INTO hackerRankItems(SlNumber, Action, HackosEarned, DateAdded, Qualifier) VALUES (?,?,?,?,?)'''
        if "logged in" in data[index][1] or "Hackos everyone" in data[index][1]:
            qualifier = "N"
        else:
            qualifier = "Y"
            selectAdd += data[index][2]
        new_entry = [data[index][0], data[index][1], data[index][2], today, qualifier]
        cur.execute(sql, new_entry[0:5])
        print("Added a line item for HackerRank.")
    
    # Add to hackerRank table
    cur.execute("SELECT * FROM hackerRank ORDER BY Date DESC LIMIT 1 ")
    last_entry = cur.fetchone()
    
    if today != last_entry[0]:
        sql = ''' INSERT INTO hackerRank(Date, Hackos, SelectHackos) VALUES (?,?,?)'''
        new_entry = [today, hackos, last_entry[2]+selectAdd]
        cur.execute(sql, new_entry[0:3])
        print("New data added to HackerRank daily table.")
    else:
        print("HackerRank was already updated today.")
    
    browser.quit() 
    return cur
    
