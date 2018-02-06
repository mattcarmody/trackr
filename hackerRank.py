# Component of trackr.py - saves data from HackerRank.com
# Requires username and password in personal.data

import bs4
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import personal

def new_date_row(sheet): 
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
        
        table = bsSoup.findAll("div", {"class":"hacko-transaction-list-view"})
        try:
            for row in table:
                temp = []
                for col in row.findAll("p"):
                    temp.append(col.text)
                data.append(temp)
        except:
            pass
        
    # Reverse order of interior lists
    data = data[::-1]
    
    # Reverse ID numbers
    for i in range(len(data)):
        data[i][0] = i+1
    
    # Put into .xlsx if it's not already there
    hrSheet = wb.get_sheet_by_name("HackerRank")
    for i, row in enumerate(data):
        if data[i][1] == hrSheet["F{}".format(i+2)].value:
            pass
        elif hrSheet["E{}".format(i+2)].value:
            print("Parsed table doesn't match log at index {}".format(i))
        else:
            hrSheet["E{}".format(i+2)].value = data[i][0]
            hrSheet["F{}".format(i+2)].value = data[i][1]
            hrSheet["G{}".format(i+2)].value = data[i][2]
            print("Added: {}, {}, {}".format(data[i][0], data[i][1], data[i][2]))
    
    newRow = new_date_row(hrSheet)
    hrSheet["A{}".format(newRow)] = "=DATE({})".format(datetime.date.today().strftime("%Y,%m,%d"))
    hrSheet["B{}".format(newRow)] = hackos
    
    browser.quit()
    
    return wb
