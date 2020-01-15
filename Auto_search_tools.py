from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time, os, fnmatch, shutil
from selenium import webdriver
import pandas as pd


def Auto_open_partsearch(partnumbers):
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    shorttime = time.strftime('%b-%d-Y', t)

    user = 'user'
    pwd = 'password'
    dates = pd.read_csv("dates.txt")
    order = pd.read_csv("order.txt")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get('https:www.autosite.com')
    driver.find_element_by_id('logonBtn').click()
    elem = driver.find_element_by_id('ctl00_ContentPlaceHolder1_UsernameTextBox')
    elem.send_keys(user)
    elem = driver.find_element_by_id('ctl00_ContentPlaceHolder1_PasswordTextBox')
    elem.send_keys(pwd)
    elem.submit()
    time.sleep(2)
    nafta = driver.find_element_by_id("tln_firstLevel").find_element_by_link_text('Region').click()
    print("logged on")
    time.sleep(3)
    applications = driver.find_element_by_id("tln_secondLevel").find_element_by_link_text('Apps').click()
    time.sleep(5)
    driver.switch_to.frame("ivuFrm_page0ivu2")
    time.sleep(10)
    driver.find_element_by_id('aaaa.SelectApp.AppName_editor.0').click()
    time.sleep(5)
    # Switch to new tab#
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    #part_search = driver.find_element_by_id('partSearch').click()
    driver.get('autosite.com')
    length = len(partnumbers)
    print(partnumbers)
    print(length)

    for number in partnumbers:
        print(number)
        print(partnumbers[0])
        if number == partnumbers[0]:
            print("if starting on " + number)
            time.sleep(5)
            part_search_form = driver.find_element_by_xpath("/html/body/form/table[1]/tbody/tr[1]/td[4]/input")
            print("clearing form")
            part_search_form.clear()  # Enter PN
            print("entering PN")
            part_search_form.send_keys(number)
            part_search_form.submit()
            print("switching off")
            #driver.find_element_by_xpath('/html/body/p').click()
            time.sleep(10)
            print("clicking input")
            driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr/td/input[2]').click()# Press search button for PN
            time.sleep(.1)
            tbl = driver.find_element_by_name('fm').get_attribute('outerHTML')
            data = pd.read_html(tbl)
            data = data[4]
            new_header = data.iloc[0]
            data = data[1:]
            data.columns = new_header
            data = data[['Model Year', 'Model Year FPV']]
            data['Part Number'] = number
            data.drop(data.tail(1).index, inplace=True)
            data.to_excel("data1.xlsx")
            continue
        else:
            print("else starting " + number)
            time.sleep(10)
            part_search_form = driver.find_element_by_xpath("/html/body/form/table[1]/tbody/tr[1]/td[4]/input")
            part_search_form.clear()
            part_search_form.send_keys(number)# Enter PN
            part_search_form.submit()
            print("switching off")
            time.sleep(5)
            print("clicking input")
            driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr/td/input[2]').click()  # Press search button for PN
            time.sleep(.1)
            tbl = driver.find_element_by_name('fm').get_attribute('outerHTML')
            df = pd.read_html(tbl)
            df = df[4]
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            df = df[['Model Year', 'Model Year FPV']]
            df['Part Number'] = number
            df.drop(df.tail(1).index, inplace=True)
            data = pd.merge(data, df, how='outer')
            data.to_excel(shorttime + ".xlsx")
            continue



partnumbers = ["xxxxx",
               "xxxxx",
               "xxxxx",
               "xxxxx"]


Auto_open_partsearch(partnumbers)
