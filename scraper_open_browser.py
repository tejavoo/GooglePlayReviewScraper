from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
import time

from optparse import OptionParser
from matplotlib.cbook import dedent
from requests_testadapter import Resp
import requests
import os
import re
import json
import pickle
from lxml import html

import codecs
import csv


chromedriver = './chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')

url = ""  # Enter url provided by scraper.py
session_id = "" #Enter session_id provided by scraper.py

driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.session_id = session_id


appname= "" #Enter app name (should be same as that used in scraper.py

wait = WebDriverWait(driver, 10)
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Counter for number of reviews scraped:
k = # Enter the review number that the scraper.py last saved.

for i in range(100):

    print("i:", i)
    #scroll till you see 'show more'
    for j in range(5):
        print('in inner loop')
        print("j:",j)
        for n in range(40):
            
            username_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k+1) + "]/div/div[2]/div[1]/div[1]/span")            
            
            try:
                username =  driver.find_element_by_xpath(username_pth).text
            except NoSuchElementException as exception: 
                print("error. Username not found")
                break
            else:
                k = k + 1
                print("review number: ",k)
               
                
            print(username)
            rating_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[1]/div[1]/div/span[1]/div/div") 
            rating = driver.find_element_by_xpath(rating_pth).get_attribute("aria-label")
            date_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[1]/div[1]/div/span[2]")
            date = driver.find_element_by_xpath(date_pth).text
            
            #Click Full Review if icon exists
            try: 
                fullRev_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div["+ str(k) +"]/div/div[2]/div[2]/span[1]/div/button")
                fullRev = driver.find_element_by_xpath(fullRev_pth)
            except NoSuchElementException as exception: 
                print("Short Review.")
                review_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[2]/span[1]")
                review = driver.find_element_by_xpath(review_pth).text
            else:
                print("Long review")
                try: 
                    fullRev.click()
                except (ElementNotVisibleException, ElementClickInterceptedException) as exception:
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    print("Element not clickable. scrolling up")
                    time.sleep(1) 
                    fullRev.click()
                #time.sleep(1)
                review_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[2]/span[2]")
                review = driver.find_element_by_xpath(review_pth).text
                               
            with open('debug/'+appname+'_username.csv',"a") as output_file:
                json.dump({"username": username},output_file)
            with open('debug/'+appname+'_rating.csv',"a") as output_file:
                json.dump({"dump_rating": rating},output_file)
            with open('debug/'+appname+'_date.csv',"a") as output_file:
                json.dump({"date": date},output_file)
            with open('debug/'+appname+'_review.csv',"a") as output_file:
                json.dump({"text": review},output_file)
            #tmp = []
            # tmp.append({"app_name":appname,
            # "username":username,
            # "rating":rating,
            # "review":review,
            # "date":date})
            
            tmp = [appname, username, rating, review, date]
    
            with open(appname+'.csv',"a") as output_file:
                fieldnames = ['app_name', 'username', 'rating','review', 'date']
                #output_file.write(str(tmp) + '\n')
                writer = csv.DictWriter(output_file, delimiter=',',fieldnames=fieldnames)
                writer.writerow({'app_name':appname,'username':username,'rating':rating,'review':review, 'date':date})
                print("saved data for:",username)
                print("\n")
                
            with open(appname+'.json',"a") as output_file:
                json.dump(tmp,output_file)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click();
    except NoSuchElementException as exception: 
        print("'Show More' not found. Continuing to scroll.")
        continue
    
#driver.quit()
