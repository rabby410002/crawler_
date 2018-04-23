# -*- coding: utf-8 -*-
import requests as r
from bs4 import BeautifulSoup
import requests
import re
import urllib
import codecs
import json
import sys

import jconfig2
import mysql.connector
import crawlerutil
import traceback
import time
from dateutil.parser import parse
from datetime import datetime
from random import randint
import json
from urllib.request import urlopen
import datetime

#https://www.urcosme.com/find-brand/766/brand_product_list?type=category

cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cnx2 = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database, charset='utf8mb4') 
cursor = cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")
cnx.commit()
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; <64-bit tags>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev> Edge/<EdgeHTML Rev>.<Windows Build>'}

global temp
global go
temp=0
go=1

def save_url(rankid,rank,last_rank,category,created,updated,prodid,prodname):
    global cnx
    global userid
    cursor = cnx.cursor()
    sql = "insert into gsearch.kr_ranking(rankid,ranking,last_rank,category_code,created_time,updated_time,prodid,prodname) values(%(rankid)s,%(ranking)s,%(last_rank)s,%(category_code)s,%(created_time)s,%(updated_time)s,%(prodid)s,%(prodname)s)" #,ptime,auther,title#,,%(a)s,%(t)s
    #print(url)
    try:
     
        cursor.execute(sql,{'rankid':rankid,'ranking':rank,'last_rank':last_rank,'category_code':category,'created_time':created,'updated_time':updated,'prodid':prodid,'prodname':prodname})#,'ptime':p,'author':a,'title':t
        cnx.commit()
        #print('ok:',url)
    except mysql.connector.DatabaseError: 
      
        error_string=traceback.format_exc() 
        #print(error_string)   
        
        #lastrank is null
        #print(rankid,rank,last_rank,category,created,updated,prodid,prodname)
        cursor.execute(sql,{'rankid':rankid,'ranking':rank,'last_rank':-1,'category_code':category,'created_time':created,'updated_time':updated,'prodid':prodid,'prodname':prodname})#,'ptime':p,'author':a,'title':t
        cnx.commit()

        '''
        #print(error_string)
        if ('Incorrect string value' and "for column 'title'" )in error_string:
            cursor.execute(sql,{'url':url,'title':'-1','pview':pview,'author':a,'ptime':p,'queryterm':queryterm})#,'ptime':p,'author':a,'title':t
            cnx.commit()
            print('Incorrect string handle done',url)
        elif 'Duplicate entry' in error_string:   
            print('url重複:',url) 
        else:
            print('other error:',url)
            print(error_string)    
        '''

def myparser(content):
    global go
    global temp
    data={}
    soup = BeautifulSoup(content, "html.parser")
    
    data=json.loads(str(soup))
   
    try:
        data[0]['category']
        
        print('hereeeeeeeeeeee')
        #jsondata = json.load(urlopen(url))
        #print(js)
        for item in data:
           
            temp=item.get("$id", "Null") #id
            print(temp)
            ranking=item.get("ranking", "Null")
            
            
            
            last_rank=item.get("lastRanking", "Null")
            
    
            category=item.get("category", "Null")
            
            created=item.get("$created", "Null")
            
            created_time=datetime.datetime.fromtimestamp(int(created)/1000.0).strftime('%Y-%m-%d %H:%M:%S')
            
            
            updated=item.get("$updated", "Null")
            updated_time=datetime.datetime.fromtimestamp(int(updated)/1000.0).strftime('%Y-%m-%d %H:%M:%S')
    
            
            
            prod= item.get("product", "Null")
            prodid=prod['$id']
            prodname=prod['name']
          
            #print("brandid:",prod['brand']['$id'])
        
            #save to sql
            ####save_url(rankid,ranking,last_rank,category)
            save_url(temp,ranking,last_rank,category,created_time,updated_time,prodid,prodname)
           
    except KeyError:
        
        go=0       
        print('go====0')
        
    except IndexError:  
        
        go=0       
        print('IndexError,go====0')  
    
    #save_to_sql(js)
    #update_page(js)
def crawl(url,cparser):
    content=getcontent(url)
    cparser(content)


def getcatelist():
    url="https://www.powderroom.co.kr/api/product-rankings/published"
    res = r.get(url,timeout=20)#,proxies=proxies
    res.encoding='utf-8'
#    SaveContentToFile(res.text)    
    content=res.text.encode('utf-8')



    soup = BeautifulSoup(content, "html.parser")
    
    data=json.loads(str(soup))
    cate=data['categories']
    cate_list=[]
    for key, value  in cate.items() :
        if key !="MAIN":
            for i in value['subCategories']:
                cate_list.append(i['code'])
        
            
    return cate_list



subcate=getcatelist()


for i in subcate:
    print(i)
    
    go=1
    temp=0  
    while go==1: #go=1代表還有資料可以抓
        print(temp)
        url="https://www.powderroom.co.kr/api/product-rankings/"+i+"?after="+str(temp)
        print(url)
        #url="https://www.powderroom.co.kr/api/product-rankings/c2100?after=26537984"
        crawlerutil.crawl(url,myparser)
        print(go)
  
     
