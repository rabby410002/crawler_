# -*- coding: utf-8 -*-
import requests as r
from bs4 import BeautifulSoup
import requests
import re
import urllib
import codecs
import json
import sys
from pprint import pprint
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

def getcontent(myurl):
    res = r.get(myurl,timeout=20)#,proxies=proxies
    res.encoding='utf-8'
#    SaveContentToFile(res.text)    
    content=res.text.encode('utf-8')

    return content



url="https://www.powderroom.co.kr/api/product-rankings/published"
content=getcontent(url)

soup = BeautifulSoup(content, "html.parser")

data=json.loads(str(soup))
cate=data['categories']
cate_list=[]
for key, value  in cate.items() :
    if key !="MAIN":
        for i in value['subCategories']:
            cate_list.append(i['code'])
    
        
print(cate_list)

    




