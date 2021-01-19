# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 10:42:08 2021

@author: Louis Régis
"""


from selenium import webdriver
import re
import time
import csv
import pandas as pd
from validate_email import validate_email

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

url = "https://not-amazon-toronto.pory.app/"




driver = webdriver.Chrome('C:\\Users\Louis Régis\.wdm\drivers\chromedriver\win32\87.0.4280.88\chromedriver.exe')


driver.get(url)

i = 0

while True:
    time.sleep(0.8)
    try: 
        driver.find_element_by_xpath("//button[@class='css-15nusyb css-63it0p css-7ai6xg bb-Box bb-Button']").click()
        container = driver.find_elements_by_xpath("//div[@class='css-1tfk13t css-63it0p css-1ur0cet bb-Box bb-ColumnsColumn']")  
        i = len(container)
        
    except: 
        False
 
business_total = []    
    
for j in range(len(container)):
    business = []
    time.sleep(2)
    title = container[j].find_element_by_xpath(".//span[contains(@class, 'css-1ystoyv css-63it0p css-ii7sgh bb-Box bb-Text')]").text
    interest = container[j].find_element_by_xpath(".//span[contains(@class, 'css-1ystoyv css-63it0p css-zbhdgm bb-Box bb-Text')]").text
    try:
        title_link = container[j].find_element_by_xpath(".//img[contains(@class, 'css-12h4bba css-63it0p css-4eq570 bb-Box bb-Image')]").click()

        time.sleep(2)
        link = container[j].find_element_by_xpath("//a[contains(@class, 'css-1l7o5eu css-63it0p css-aqjbqz bb-Box bb-Button')]").get_attribute("href")
    
        close_button = container[j].find_element_by_xpath("//button[contains(@class, 'css-1pzmiu1 css-1fbr0b8 css-63it0p css-n623by css-1fie8gx css-jwhr8m bb-Box bb-ModalDisclosure bb-Button bb-ButtonClose')]").click()
    except: 
        link="na"

    
    business.extend([title, link, interest])
    business_total.append(business)
    print(business)
driver.close()

df = pd.DataFrame(business_total, columns=['title', 'link', 'interest'])


lines = []

print(lines)

for url in df["link"]:

    url_list = set()
    driver2 = webdriver.Chrome('C:\\Users\Louis Régis\.wdm\drivers\chromedriver\win32\87.0.4280.88\chromedriver.exe')
    try: 
        driver2.get(url)        
        doc = driver2.page_source
        matches = ["png", "jpg", "JPG"]
    
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', doc)
        
            
        for email in emails:
            if any(x in email for x in matches):
                url_list = set()
            else:     
                url_list.add(email) 
        url_list = list(url_list)
        
        print(url_list)
        lines.append(url_list)
        print(lines)
        driver2.close()
    except: 
        url_list = []
        lines.append(url_list)
        driver2.close()

  
print(lines)    
    
df["email"] = lines


for line in df["email"]: 
    if len(line) == 0: 
        pass
    elif len(line) == 1:
        for x in line: 
          
            is_valid = validate_email(x)

            if is_valid == True: 
                print("validated")
                print(x)
            else: 
                x = "na"
    else: 
        validated_email = []
        for x in line: 
            is_valid = validate_email(x)
            print(is_valid)
    
            if is_valid == True: 
                print("validated")
                print(x)
            else: 
                x = "na"
                
    #https://stackoverflow.com/questions/51495800/pandas-python-how-to-create-multiple-columns-from-a-list

df.to_csv("backup file.csv")
