# Component of trackr.py - saves data from HackerRank.com
# Requires username and password in personal.data

import bs4
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import personal

def update_HackerRank(wb):
    url = "https://www.hackerrank.com/" + personal.data["hrUsername"]

    browser = webdriver.Firefox()
    browser.get(url)
    loginElem = browser.find_element_by_class_name("login").click()

    username = browser.find_element_by_name("login")
    username.send_keys(personal.data["hrUsername"])

    password = browser.find_element_by_name("password")
    password.send_keys(personal.data["hrPassword"])
    password.send_keys(Keys.RETURN)

    hackosUrl = "https://www.hackerrank.com/" + personal.data["hrUsername"] + "/hackos"
    browser.get(hackosUrl)
    browser.refresh()

    innerHTML = browser.execute_script("return document.body.innerHTML")
    bsSoup = bs4.BeautifulSoup(innerHTML, "lxml")
    h3 = bsSoup.find("h3")

    hackosRegex = re.compile(r"Total Hackos: (\d*)")
    mo = hackosRegex.search(h3.text)
    hackos = int(mo.group(1))

    hrSheet = wb.get_sheet_by_name("HackerRank")
    newRow = hrSheet.max_row + 1
    hrSheet["A" + str(newRow)] = datetime.date.today().strftime("%B %d, %Y")
    hrSheet["B" + str(newRow)] = hackos
    
    browser.quit()
    
    return wb
