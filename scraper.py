# -*- coding: UTF-8 -*-

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
import random
from lxml import html

import codecs
import csv


chromedriver = "C:/Users/teja/Downloads/chromedriver/chromedriver_win32/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600') # optional
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

driver.get("https://play.google.com/store/apps/details?id=com.ubercab.eats&showAllReviews=true")  # Replace APP_ID with ID of app of interest
appname= "uber_eats_reviews" # The name of the app- the json files will be named as per this field

wait = WebDriverWait(driver, 10)
SCROLL_PAUSE_TIME = 0.5

# Changer order to Newest First
driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div/div").click()
time.sleep(3)

# click newest here.
driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]").click()
time.sleep(1)

url = driver.command_executor._url       
session_id = driver.session_id      

print(url)
print(session_id)
   

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Counter for number of reviews scraped:
k = 0

for i in range(500):

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
                               

            with open('data_folder/'+appname+'_data.csv',"a",encoding='utf-8',newline='') as output_file:
                row = [username, rating[6], date, review]
                # print(row)
                writer = csv.writer(output_file)
                writer.writerow(row)
                # json.dump({"username": username, "dump_rating": rating,"date": date, "text": review },output_file)
            # with open('debug/'+appname+'_username.csv',"a") as output_file:
            #     json.dump({"username": username},output_file)
            # with open('debug/'+appname+'_rating.csv',"a") as output_file:
            #     json.dump({"dump_rating": rating},output_file)
            # with open('debug/'+appname+'_date.csv',"a") as output_file:
            #     json.dump({"date": date},output_file)
            # with open('debug/'+appname+'_review.csv',"a") as output_file:
            #     json.dump({"text": review},output_file)
            
            tmp = [appname, username, rating, review, date]
    
            # with open(appname+'.csv',"a") as output_file:
            #     fieldnames = ['app_name', 'username', 'rating','review', 'date']
            #     #output_file.write(str(tmp) + '\n')
            #     writer = csv.DictWriter(output_file, delimiter=',',fieldnames=fieldnames)
            #     try:
            #         writer.writerow({'app_name':appname,'username':username,'rating':rating,'review':review, 'date':date})
            #     except UnicodeEncodeError as excep:
            #         pass
                # print("saved data for:",username)
                # print("\n")
            print("saved data for:",username)
            print("\n")

            # with open(appname+'.json',"a") as output_file:
            #     json.dump(tmp,output_file)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click();
        time.sleep(1)     
    except NoSuchElementException as exception: 
        print("'Show More' not found. Continuing to scroll.")
        continue

