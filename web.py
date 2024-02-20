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

#função para baixar uma imagem

def abaixaUmaImagem(link,local, post_id):
  success = False
  for i in range(0, 10):
    try:
      driver.get(link)
      soup = BeautifulSoup(driver.page_source, "html.parser")
      div = soup.find_all(class_="css-175oi2r r-1p0dtai r-1d2f490 r-u8s1d r-zchlnj r-ipm5af r-1loqt21")
      print(div)
      if (len(div)==0): 
        return {"success": True, "message": "Post without Image"}
      imageUrl = div[0].img.get("src")
      urllib.request.urlretrieve(imageUrl,local)
      success = True
      time.sleep(2)
      return {"success": True, "message": "Success"}
    except Exception as e:
      print(e)
      time.sleep(10)
    return {"success": False, "message": "Fail"}    


#Dicionários com os links
url_images_path = "2018"
candidatosArq = os.listdir(url_images_path)
candidatosInfo = {}
nomeCandidatos = []
for cand in candidatosArq:
    candidatosInfo[cand[:-12]] = {}
    nomeCandidatos.append(cand[:-12])
    dateCandidate = pd.read_csv("2018/"+cand, sep=",")
    tweetID = dateCandidate["Tweet ID"]
    tweetUrl = dateCandidate["URL"]
    i=0
    for id in tweetID:
        id = id[3:]
        candidatosInfo[cand[:-12]][id] = tweetUrl[i]
        i+=1

#Login
info_path = 'twitter.txt'
with open(info_path, "r") as arquivo:
  info = arquivo.readlines()
nameUser = info[0][6:-1]
mailUser = info[1][7:-1]
userPassword = info[2][10:]

options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://twitter.com/i/flow/login")
time.sleep(2)
userMail = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
userMail.send_keys(mailUser)
userMail.send_keys(Keys.ENTER)
time.sleep(20)
userName = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="on"]')))
userName.send_keys(nameUser)
userName.send_keys(Keys.ENTER)
password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
password.send_keys(userPassword)
password.send_keys(Keys.ENTER)
time.sleep(20)


#testando uma imgaem
abaixaUmaImagem("https://twitter.com/alvarodias_/status/1132725156676288512", './imagensCandidatos/teste.png')
# for candidato in nomeCandidatos:
#   for id in list(candidatosInfo[candidato].values()):
#     abaixaUmaImagem(candidatosInfo[candidato][id], './imagensCandidatos/'+candidato+"/"+id+".png")

driver.quit()
print("Terminei")
