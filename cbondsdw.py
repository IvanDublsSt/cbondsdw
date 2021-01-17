from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import os
import time
import random
from PIL import Image
from io import BytesIO
import urllib.request
import urllib.request



def open_cbonds(login = "isdublenskiy@edu.hse.ru", password = "1234567890", begin = "01.01.2015", end = "31.12.2020", newdriver = True, executable_path = r"chromedriver.exe"):
    global driver
    print("Opening Cbonds")
    if newdriver == True:
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
    else:
        driver.refresh()
    driver.get("http://old.cbonds.ru/quotes/")
    elem = driver.find_element_by_xpath("//input[@id='auth_login']")
    elem.send_keys(login)
    elem = driver.find_element_by_xpath("//input[@id='auth_pwd']")
    elem.send_keys(password)
    elem = driver.find_element_by_xpath("//input[@type='submit' and @value = 'Вход']")
    elem.click()
    try: 
        driver.find_element_by_xpath("//img[@src = '/dbcmd/includes/widgets/CBSearchTemplate/templates/cbonds_v2/images/pro_ico_a.gif']")
        driver.refresh()
        elem = driver.find_element_by_xpath("//input[@id='auth_login']")
        elem.send_keys(login)
        elem = driver.find_element_by_xpath("//input[@id='auth_pwd']")
        elem.send_keys(password)
        elem = driver.find_element_by_xpath("//input[@type='submit' and @value = 'Вход']")
        elem.click()        
    except:
        try:
            elem = driver.find_element_by_xpath("//a[@class = 'cookie_panel_success js_cookie_panel_success']")
            elem.click()
        except:
            pass
        elem = driver.find_element_by_xpath("//*[@id='CbQuotesSearchForm']/div[8]/div[1]/div/a")
        elem.click()
        try:
            elem = driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_from hasDatepicker']")
            elem.clear()
            elem.send_keys(begin)
            elem = driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_to hasDatepicker']")
            elem.clear()
            elem.send_keys(end)
        except:
            driver.refresh()
            elem = driver.find_element_by_xpath("//*[@id='CbQuotesSearchForm']/div[8]/div[1]/div/a")
            elem.click()
            try:
                elem = driver.find_element_by_xpath("//a[@class = 'cookie_panel_success js_cookie_panel_success']")
                elem.click()
            except:
                pass
        elem = driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_from hasDatepicker']")
        elem.clear()
        elem.send_keys(begin)
        elem = driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_to hasDatepicker']")
        elem.clear()
        elem.send_keys(end)    
        try:
            elem = driver.find_element_by_xpath("//a[@class = 'cookie_panel_success js_cookie_panel_success']")
            elem.click()
        except:
            pass
    return(driver)

def dates_correct(begin = "01.01.2015", end = "31.12.2020"):
    global driver
    try: 
        elem = driver.find_element_by_xpath("//div[@aria-describedby = 'one-emisison-limit-message-container']")
        elem.send_keys(Keys.ESCAPE)
    except: 
        pass
    elem = driver.find_element_by_xpath("//span[@class = 'datepickerRange-right-input']")
    if elem.get_attribute("style") == "display: none;":
        elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[3]/div[3]/form/div[5]/table/tbody/tr[1]/td[2]/span[3]/div/div/p/span")
        elem.click()
        elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[3]/div[3]/form/div[5]/table/tbody/tr[1]/td[2]/span[3]/div/div/div/div/div[1]/div[2]/span[2]")
        elem.click()
        elem = driver.find_element_by_xpath("//input[@placeholder = 'Эмитент № Гос.рег ISIN']")
        elem.clear()
        elem.send_keys("RU000A")
        time.sleep(1)
        elem.send_keys("0ZYUJ0")
        time.sleep(15)
        elem2 = driver.find_element_by_xpath("//ul[@id = 'ui-id-5' and @class = 'ui-autocomplete ui-front ui-menu ui-widget ui-widget-content cb-suggest']")
        elem3 = elem2.find_element_by_xpath(".//li")
        elem4 = elem3.find_element_by_xpath(".//a")
        elem4.click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//input[@data-init_filter = 'emission' and @value = 'Выбрать']")
        elem.click()
        elem = driver.find_element_by_xpath("//input[@type = 'radio' and @name = 'mode' and @value = '1']")
        elem.click()
        elem = driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_from hasDatepicker']")
        elem.clear()
        elem.send_keys(begin)
        elem = driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_to hasDatepicker']")
        elem.clear()
        elem.send_keys(end)
        print("corrected dates")
        
        
def PrimaryDownloadCbonds(bondlist, login = "isdublenskiy@edu.hse.ru", password = "1234567890", begin = "01.01.2015", end = "31.12.2020", executable_path = r"chromedriver.exe", bigbondlist = []):
    global driver
    #define variables
    print("")
    print("Download is started")
    if bigbondlist == []:
        bigbondlist = bondlist
    #print(driver)
    names = []
    badnames = []
    badcheck = 0
    found_nothing = []
    found_too_much = []
    
    #check for driver to be open
    def driver_check():
        global driver
        print("driver check")
        try:
            driver.find_element_by_xpath("//body")
            driver_on = 1
        except:
            driver_on = 0
        if driver_on == 0:
            open_cbonds(login, password, newdriver = True, executable_path = executable_path)
        else:
            pass
    
    #check for pro message or pro sign in dates
    def check_pro_message():
        global driver
        pro_message_check = 1
        while pro_message_check == 1:
            try:
                driver.find_element_by_xpath("//a[@href = 'http://cbonds.ru/about/paccess.php']")
                pro_message_check = 1
            except:
                pro_message_check = 0
            try:
                driver.find_element_by_xpath("//img[@src = '/dbcmd/includes/widgets/CBSearchTemplate/templates/cbonds_v2/images/pro_ico_a.gif']")
                pro_message_check = 1
            except:
                pass

            if pro_message_check == 1:
                print("pro blocked")
                driver.close()
                if driver is not None:
                    driver = None  
                open_cbonds(login, password, newdriver = True, executable_path = executable_path)
        
    
    
    #check for cookies message
    def check_cookies():
        print("cookies check")
        global driver
        cookies_message_check = 1
        while cookies_message_check == 1:
            try:
                elem = driver.find_element_by_xpath("//a[@class = 'cookie_panel_success js_cookie_panel_success']")
                elem.click()
            except:
                cookies_message_check = 0
    
    #check for dates correctness:
    def dates_check_local():
        print("dates check")
        global driver
        dates_are_wrong = 1
        try:
            driver.find_element_by_xpath("//input[@class='oform_date_input datepicker tradings-date_to hasDatepicker']").click()
            dates_are_wrong = 0
        except:
            dates_are_wrong = 1
        if dates_are_wrong == 1:
            check_pro_message()
            check_cookies()
            print("wrong dates")
            dates_correct(begin, end)
            check_pro_message()
            check_cookies()
    
    #check for issuer window to be open:
    def check_issuer_window():
        print("issuer check")
        global driver
        issuer_open = 1
        try:
            driver.find_element_by_xpath("//input[@class = 'oform_input_text cb-suggest-input ui-autocomplete-input' and @placeholder = 'Эмитент']").click()
        except:
            issuer_open = 0
        if issuer_open == 1:
            driver.find_element_by_xpath("//*[@id='emitentContainer']/div/div/p/span").click()
    
    #try doing everything in normal way 
    def normal_way(issue):
        global driver
        problems = 1
        print("normal way for " + issue)
        i_beg = issue[0:(round(len(issue)/2))]
        i_end = issue[(len(i_beg)):(len(issue))]
        try:
            #click
            try:
                driver.find_element_by_xpath("//input[@placeholder = 'Эмитент № Гос.рег ISIN']").click()
                driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[3]/div[3]/form/div[5]/table/tbody/tr[1]/td[2]/span[3]/div/div/p/span").click()
            except:
                pass
            issuer_open = 0
            elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[3]/div[3]/form/div[5]/table/tbody/tr[1]/td[2]/span[3]/div/div/p/span")
            elem.click()
            print("clicked emission button for " + issue)
            elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div[3]/div[3]/form/div[5]/table/tbody/tr[1]/td[2]/span[3]/div/div/div/div/div[1]/div[2]/span[2]")
            elem.click()
            print("cleared list for " + issue)
            elem = driver.find_element_by_xpath("//input[@placeholder = 'Эмитент № Гос.рег ISIN']")
            elem.clear()
            elem.send_keys(i_beg)
            time.sleep(1)
            elem.send_keys(i_end)
            time.sleep(11)
            print("typed " + issue)
            elem2 = driver.find_element_by_xpath("//ul[@id = 'ui-id-5' and @class = 'ui-autocomplete ui-front ui-menu ui-widget ui-widget-content cb-suggest']")
            elem3 = elem2.find_element_by_xpath(".//li")
            elem4 = elem3.find_element_by_xpath(".//a")
            elem4.click()
            print("chosen " + issue)
            elem = driver.find_element_by_xpath("//input[@data-init_filter = 'emission' and @value = 'Выбрать']")
            elem.click()
            #print("chosen again for " + issue)
            elem = driver.find_element_by_xpath("//input[@type = 'submit' and @value = 'Найти']")
            elem.click()
            print("finished search for " + issue)
           # time.sleep(60)
            #check whether we found anything:
            found_nothing = True
            try:
                elem = driver.find_element_by_xpath("//div[@id = 'emissions-statistics']")
                elem2 = elem.find_element_by_xpath("//div[@style = 'float:left; margin-right:30px;']")
                if 'Найдено эмиссий (на текущую дату): 0' in elem2.text:
                    print("found nothing for " + issue)
                else:
                    found_nothing = False
            except:
                found_nothing = False
            #check if we found too much
            found_too_much = True
            try:
                driver.find_element_by_xpath("//td[@style = 'color: red !important']")
            except:
                found_too_much = False
                
                
            if (found_nothing == False) and (found_too_much == False):
                elem2 = driver.find_element_by_xpath("//a[@class = 'toolbtn export-excel-btn export-excel-btn-rus']")
                elem2.click()
                print("pressed saving for " + issue)
                print("finished " + issue)
            problems = 0
            
        except:
            print("problems")
            found_nothing = False
            found_too_much = False
            pass
        
        return([problems, found_nothing, found_too_much])
    
    print("pre-check")
    driver_check()
    check_pro_message()
    check_cookies()
    dates_check_local()
    #check_issuer_window()    
    
    
    #The Loop
    for i in bondlist:
        start = time.time()
        print("started " + i)
        print("Bond number " + str(bigbondlist.index(i)))
        results = normal_way(i)
        problems = results[0]
        names.append(i)
        #we got a problem and trying to correct problems on the run
        if problems == 1:
            print("post-check")
            try:
                driver_check()
                check_pro_message()
                check_cookies()
                dates_check_local()
            except:
                pass
            #check_issuer_window()
            #check wheter we were able to solve it 
            try:
                print("try again")
                results = normal_way(i)
            except:
                print("bad error")
                badnames.append(i)
                results = [1,False, False]
        #whatever happened, we are saving results 
        found_nothing.append(results[1])
        found_too_much.append(results[2])
        print(time.time() - start)
    return([names, found_nothing, found_too_much, badnames])
    
        
        
def RepeatDownloadCbonds(bondlist, login = "isdublenskiy@edu.hse.ru", password = "1234567890", begin = "01.01.2015", end = "31.12.2020", executable_path = r"chromedriver.exe", bigbondlist = [], path = "C://Users//Fride//Downloads"):
    file = open(path+ "//found_nothing"+ str(time.time()) + ".txt", "w")
    file2 = open(path+ "//found_too_much"+ str(time.time()) + ".txt", "w")
    file3 = open(path+ "//bad_results"+ str(time.time()) + ".txt", "w")
    try:
        driver
    except:
        open_cbonds(login = login, password = password, begin = begin, end = end, newdriver = True, executable_path = executable_path)

    print("started the repetitive process")
    badnamesold = []
    found_nothing = []
    found_too_much = []
    badcheck = 0
    results = PrimaryDownloadCbonds(bondlist, login, password, begin, end, executable_path, bigbondlist)
    badnames = results[3]
    found_nothing += list(np.array(results[0])[results[1]])
    found_too_much += list(np.array(results[0])[results[2]])
    #badnames = [i for i in results[0] if  (( i not in found_nothing) and (i not in found_too_much))]
    while ((badnamesold != badnames) and (badnames != [])) or (badcheck == 1):
        print("repeat gain")
        if driver is None:
            open_cbonds(login, password, begin, end, executable_path = executable_path)
            
        badnamesold = badnames.copy()
        results = PrimaryDownloadCbonds(badnames, login, password, begin, end, executable_path, bigbondlist)
        badnames = results[3]
        found_nothing += list(np.array(results[0])[results[1]])
        found_too_much += list(np.array(results[0])[results[2]])
    print("finished repeats")
    for i in found_nothing:
        file.write(i + ",")
    file.close()
    for i in found_too_much:
        file2.write(i + ",")
    file2.close()
    if badnamesold != []:
        for i in badnamesold:
            file3.write(i + ",")
        file3.close()
    else:
        file3.close()
    #for i in status:
        #file2.write(i + ",")
    #file2.close()        
        
        
def LongListDownloadCbonds(bondlist, login = "isdublenskiy@edu.hse.ru", password = "1234567890", begin = "01.01.2015", end = "31.12.2020", executable_path = r"chromedriver.exe", bigbondlist = [], path = "C://Users//Fride//Downloads"):
    if bigbondlist == []:
        bigbondlist = bondlist
    if len(bondlist) <= 50:
        RepeatDownloadCbonds(bondlist, login = login, password = password, begin = begin, end = end, path = path, executable_path = executable_path, bigbondlist = bigbondlist)
    else:
        number_of_full_iterations = len(bondlist)//50
        remained_iteration = len(bondlist)%50
        for i in range(number_of_full_iterations):
            i+=1
            print("From " + str((i-1)*50) + " to " + str(i*50))
            RepeatDownloadCbonds(bondlist[((i-1)*50):(i*50)], login = login, password = password, begin = begin, end = end, path = path, executable_path = executable_path, bigbondlist = bigbondlist)
        print("From " + str(number_of_full_iterations*50) + " to " + str(number_of_full_iterations*50 + remained_iteration))
        RepeatDownloadCbonds(bondlist[(number_of_full_iterations*50):(number_of_full_iterations*50 + remained_iteration)], login = login, password = password, begin = begin, end = end, path = path, executable_path = executable_path, bigbondlist = bigbondlist)

