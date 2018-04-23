#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import urllib
import sys
import re
from selenium import webdriver
import urllib.parse
#import peewee
#from peewee import *
#from playhouse.db_url import connect
from selenium.webdriver.chrome.options import Options
import os
import jconfig2
#import MySQLdb
import mysql.connector
#import pymysql
import socket
import traceback
import datetime
import datetime
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 

def save_data(data):
    global cnx
    cursor = cnx.cursor()
    sql = "insert into gsearch.googleresult(begindate,enddate,keyword,numresult) values(%(begindate)s,%(enddate)s,%(keyword)s,%(numresult)s)  ON DUPLICATE KEY UPDATE numresult=%(numresult)s  "
    try:
        print(data) 
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()


def get_progress(query):
    global cnx
    cursor = cnx.cursor()
    sql = "select min(enddate) from googleresult where keyword='"+query+"'  "
    #resultdt=datetime.datetime.now().date()
    resultdt=datetime.datetime.strptime("2017-12-30","%Y-%m-%d").date()
    try:
#        print(sql)
        cursor.execute(sql)
        for u in cursor:
            resultdt=u[0]
    except: 
        print('exception')
        traceback.print_exc()
    return resultdt


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.binary_location='/usr/bin/google-chrome'
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.

#options.binary_location='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
#driver = webdriver.Chrome('C:\\portable\\chromedriver.exe',chrome_options=options)  # Optional argument, if not specified will search path.





def process_page(driver):
    html = driver.page_source
    soup = BeautifulSoup(html)
    elmt=soup.find('div',{'id':'resultStats'})
    print(elmt.text)
    sresult=re.search(u'約有 (.+) 項結果',elmt.text)
    if sresult is None:
        sresult=re.search(u'(.+) 項結果',elmt.text)
    print(sresult)
    print(sresult.group(1))
    return sresult.group(1).replace(",","")

    
#    elmts=driver.find_elements_by_xpath("//div[@id='resultStats']")
#    for elmt in elmts:
#        print(elmt)
#        print("text="+elmt.text)
#        sresult=re.search(u'約有 (.+) 項結果',elmt.text)
        
##        print(sresult)
#        print(sresult.group(1))
#        return sresult.group(1)
        


def get_prevweek(dt):
    ed=dt.strftime("%m/%d/%Y").replace("/","%2F")
    dt=dt+timedelta(days=-6)
    bg=dt.strftime("%m/%d/%Y").replace("/","%2F")
    return (bg,ed)




def mysearch(dt,query):
    global enddate
    global driver
#    n= datetime.datetime.now()
    bg,ed=get_prevweek(dt)
    fullurl='https://www.google.com.tw/search?rlz=1C1CHZL_enTW725TW725&biw=1243&bih=666&tbs=cdr%3A1%2Ccd_min%3A'+bg+'%2Ccd_max%3A'+ed+'&ei=DLJKWqXSLoaA8QXv9LagCg&q='+query+'&oq='+query
    print(fullurl)
    driver.get(fullurl)
    try:
        #搜尋結果為0的時候這一行會timeout error,所以做except例外處理,給值:0
        ww = WebDriverWait(driver,12).until(EC.presence_of_element_located((By.XPATH, "//div[@id='resultStats'][string-length(text()) > 1]")))
        numresult=process_page(driver)
        save_data({'begindate':dt+timedelta(days=-6),'enddate':dt,'keyword':query,'numresult':int(numresult)})
        time.sleep(2)
    except:
        save_data({'begindate':dt+timedelta(days=-6),'enddate':dt,'keyword':query,'numresult':0})
        time.sleep(2)


enddate=datetime.datetime.strptime("2015-01-01","%Y-%m-%d")
n=datetime.datetime.strptime("2017-12-30","%Y-%m-%d")
#n=datetime.datetime.strptime("2016-09-15","%Y-%m-%d")


#result=['美眉特色畫筆+1028','毛孔+無痕慕絲+1028','柔礦BB隔離乳+1028','無極限黑絨+1028','啵亮完妝水+1028','輪廓餅+1028']

cursor = cnx.cursor()
sql="SELECT distinct keyword FROM gsearch.googleresult_old where keyword not in (select distinct keyword from gsearch.googleresult)"
cursor.execute(sql)
result=[]
for u in cursor:   # 把要跑的keyword存到result list
    result.append(u[0])

for query in result:  

    #query="亮頰透漾腮紅+1028"
    
    n=get_progress(query)
    if n is None:
        n=datetime.datetime.strptime("2017-12-30","%Y-%m-%d").date()
        
    print(n)
    
    while n >= enddate.date():
        mysearch(n,query)
        n=n+timedelta(days=-7)
   


driver.close()
exit(1)


