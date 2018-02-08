# Component of trackr.py - saves data from HackerRank.com
# Requires username and password in personal.data

import bs4
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import personal

today = "=DATE({})".format(datetime.date.today().strftime("%Y,%-m,%-d"))

def new_date_row(sheet): # Because two tables share the HackerRank xlsx sheet
    check_row = sheet.max_row
    while sheet["A{}".format(check_row)].value == None:
        check_row -= 1
    check_row += 1
    return check_row

def update_HackerRank(wb):
    url = "https://www.hackerrank.com/{}".format(personal.data["hrUsername"])

    browser = webdriver.Firefox()
    browser.get(url)
    loginElem = browser.find_element_by_class_name("login").click()

    username = browser.find_element_by_name("login")
    username.send_keys(personal.data["hrUsername"])

    password = browser.find_element_by_name("password")
    password.send_keys(personal.data["hrPassword"])
    password.send_keys(Keys.RETURN)

    data = []
    for page in range(1, 4):
        hackosUrl = "https://www.hackerrank.com/{}/hackos/page/{}".format(personal.data["hrUsername"], page)
        browser.get(hackosUrl)
        
        # Often has a 404 error, but refreshing helps
        count = 0
        while count < 15:
            innerHTML = browser.execute_script("return document.body.innerHTML")
            bsSoup = bs4.BeautifulSoup(innerHTML, "lxml")
            try:
                h3 = bsSoup.find("h3")
                if "Hackos" in h3.text:
                    break
            except:
                count += 1
                browser.refresh()
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
        
    # Reverse order of table rows
    data = data[::-1]
    
    # Renumber IDs (reverse direction)
    for i in range(len(data)):
        data[i][0] = i+1
    
    # Put each new line item in .xlsx
    hrSheet = wb.get_sheet_by_name("HackerRank")
    selectAdd = 0
    for i, row in enumerate(data):
        if data[i][1] == hrSheet["F{}".format(i+2)].value:
            pass
        elif hrSheet["E{}".format(i+2)].value:
            print("Parsed table doesn't match log at index {}".format(i))
        else:
            hrSheet["E{}".format(i+2)].value = data[i][0]
            hrSheet["F{}".format(i+2)].value = data[i][1]
            hrSheet["G{}".format(i+2)].value = data[i][2]
            hrSheet["H{}".format(i+2)].value = today
            print("Added: {}, {}, {}".format(data[i][0], data[i][1], data[i][2]))
            # Add in identifier if line item meets exercise criteria
            if "logged in" in data[i][1] or "Hackos everyone" in data[i][1]:
                hrSheet["I{}".format(i+2)].value = "N"
            else:
                hrSheet["I{}".format(i+2)].value = "Y"
                selectAdd += data[i][2]
    
    # Add new daily values to .xlsx
    newRow = new_date_row(hrSheet)
    if not hrSheet["A{}".format(newRow-1)].value == today:
        hrSheet["A{}".format(newRow)] = today
        hrSheet["B{}".format(newRow)] = hackos
        hrSheet["C{}".format(newRow)] = int(hrSheet["C{}".format(newRow-1)].value) + selectAdd
        print("Updated HackerRank daily totals.")
    else:
        print("HackerRank already has totals for today.")
    
    browser.quit()
    
    return wb
