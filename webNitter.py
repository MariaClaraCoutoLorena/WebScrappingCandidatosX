from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from urllib.parse import urljoin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import pandas as pd
import urllib.request
import re


def abaixarfoto():
    print("Cheguei na foto")

def AjustarData(spanString):
    procurado = re.findall('title=".*UTC',str(spanString))
    if(len(procurado)>0): procurado = procurado[0][7:-14]
    return procurado

nameProfile1 = '@jairbolsonaro'

options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://nitter.poast.org/")
time.sleep(2)
userMail = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))
userMail.send_keys(nameProfile1)
userMail.send_keys(Keys.ENTER)
time.sleep(3)
userLink = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/jairbolsonaro"]')))
userLink.send_keys(Keys.ENTER)
time.sleep(2)


#chegar ate a epoca certa
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    spans = soup.find_all(class_="tweet-date")
    spansDate = list(map(AjustarData, spans))
    print(spansDate)
    for i in reversed(range(1,32)):
        dataCerta = 'Out '+str(i)+', 2022' in spansDate
        if dataCerta: break
    if dataCerta:
        print('Cheguei na época certa')
        break
    else:
        continueLink = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="href="?cursor=DAABCgABGFBOCwo__-kKAAIYQ7C_hFeReggAAwAAAAIAAA""]')))
        continueLink.send_keys(Keys.ENTER)
        time.sleep(2)
        break

time.sleep(20)

driver.quit()
print("Terminei")
