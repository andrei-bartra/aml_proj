# -*- coding: utf-8 -*-
'''
  _____________________________________________
 |                                             |
 | Webscrapping of REV Political Transcripts   |
 | Authors: - Andrei Batra                     |
 | Date: May, 2021                             |
 |_____________________________________________|


 =============================================================================
 Webscrapping of resume data from JNE website:
     https://www.rev.com/blog/transcript-category/political-transcripts/
 =============================================================================
'''


#  ________________________________________
# |                                        |
# |              1: Libraries              |
# |________________________________________|

#Basics
import os, sys

##selenium
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC


#Other libraries
import time

#Local modules
#import admin
import ws_ugly_stuff as ug


# Path Settings
#os.chdir(admin.wd)
#sys.path.append(os.chdir(admin.wd))


# Key Control
print('Loading Web Scrapper Lord {}'.format(os.environ['USERNAME']))
if os.environ['USERNAME'] == 'Tato':
    cmd_key = Keys.COMMAND

elif os.environ['USERNAME'] == 'andrei':
    cmd_key = Keys.CONTROL

elif os.environ['USERNAME'] == 'andre':
    cmd_key = Keys.CONTROL

#  ________________________________________
# |                                        |
# |               3: Crawler               |
# |________________________________________|



def crawler(load_time=1,  test=None):
    options = webdriver.ChromeOptions()
    p = {"download.default_directory": ug.dpath, "safebrowsing.enabled":"false"}
    options.add_experimental_option("prefs", p)
    driver = Chrome(ug.driver_path, options=options)
    driver.get(ug.url)
    driver.maximize_window()
    i = 0
    while True:
        if i==test:
            break
        page_bar = driver.find_element_by_xpath(ug.xpaths['nbar'])
        next_button = page_bar.find_elements(By.TAG_NAME, "li")[-1]
        if next_button.text != 'NEXT »':
            break
        rev_list = driver.find_elements_by_class_name("fl-post-column")
        for rev in rev_list:
            ActionChains(driver).move_to_element(rev).key_down(cmd_key).\
                click(rev).key_up(cmd_key).perform()
            time.sleep(load_time)
            driver.switch_to.window(driver.window_handles[1])
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(load_time)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(load_time)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            try:
                driver.find_element_by_xpath(ug.xpaths['link']).click()
            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue
            time.sleep(load_time)
            driver.find_element_by_xpath(ug.xpaths['dwld']).click()
            time.sleep(load_time + 1)
            select = Select(driver.find_element_by_xpath(ug.xpaths['type']))
            select.select_by_value('4')
            body = driver.find_element_by_class_name("modal-body")
            xport = body.find_elements(By.TAG_NAME, "button")[0]
            xport.click()
            time.sleep(load_time)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            i += 1
            print('saving transcript {}'.format(i))
            if i==test:
                break
        next_button.click()
        time.sleep(load_time + 2)






#  ________________________________________
# |                                        |
# |            4: Cpnsolidation            |
# |________________________________________|