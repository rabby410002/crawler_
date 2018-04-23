# -*- coding: euc-kr -*-
import requests as r
import mysql.connector
import jconfig2
import re
import traceback
import random
import pickle
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; <64-bit tags>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev> Edge/<EdgeHTML Rev>.<Windows Build>'}

proxylist=pickle.load(open("proxy.pkl" , "rb"))

def extract_digit(txt):
    m=re.search(r'([\d\.\,]+)',txt)
    if m:
        ans=m.group(1)
        return ans.replace(",","")
    else:
        return -1

def save_elements(cnx2,sql,data):
    cursor2 = cnx2.cursor()
    
    
    
    try:
        cursor2.execute(sql,data)
        cnx2.commit()
        print('ok')
    
    except mysql.connector.DatabaseError: 
        print('exception:DatabaseError')
        #print(contentparser.content.text)
        traceback.print_exc()
        #sql="update pixnet_post_makeupsharing set content='-1' where url=%(url)s"

        #data={"content":content.text,"url":url}
        #data={"content":'-1111',"url":'-1'}
        #print(sql)
        #print(data)
        cursor2.execute(sql,data)
        cnx2.commit()

'''    
def getcontent(myurl):
    
    global proxylist
    #print(proxylist)
    proxies=random.choice(proxylist)
    
    

#http://14.203.99.67:8080


    try:
        #s = r.Session()
        proxies = {'http': 'http://12.129.82.194:8080','https': '12.129.82.194:8080'}
        #s.proxies = proxies
        print(proxies)
        print(myurl)
        print(headers)
        
        res = r.get(myurl,headers=headers,proxies=proxies)
        #res = s.get(myurl,headers=headers)

#        res = r.get(myurl,headers=headers,proxies=proxies)
        res.encoding='utf-8'
#    SaveContentToFile(res.text)       


        
        
        content=res.text.encode('utf-8')
    except Exception:
        print("exception")
        traceback.print_exc()
        return None
    return content
'''

def getcontent(myurl):
    
    #proxies = {'http': 'http://183.111.169.203:3128','https': '183.111.169.203:3128'}
    #proxies =  {'http': 'http://186.46.94.18:65301','https': 'http://186.46.94.18:65301'}


    done=0
    count=0
    while done==0:
        count+=1
        if count<=30:
            try:
     
                res = r.get(myurl,headers=headers,timeout=20)#,proxies=proxies
                done=1
            except:
                print('except res')
                #traceback.print_exc()
                continue    
        else:
            print('no response',myurl)   
            break 

                    
    #res = r.get(myurl,headers=headers)

    res.encoding='utf-8'
#    SaveContentToFile(res.text)    
    content=res.text.encode('utf-8')

    return content



def get_job(logtype):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    sql = "select param from crawler_log where logtype='"+logtype+"' order by logtime desc"
    cursor.execute(sql)
    for (u) in cursor:
        return u[0]

def log_next(logtype,param):
    cnx = mysql.connector.connect(user=jconfig2.user, password=jconfig2.password,host=jconfig2.host,port=jconfig2.port,database=jconfig2.database) 
    cursor = cnx.cursor()
    sql = "insert into crawler_log(logtype,param,logtime) values(%(logtype)s,%(param)s,NOW())"

    data={'logtype':logtype,'param':param}
    try:
        cursor.execute(sql,data)
        cnx.commit()
    except: 
        print('exception')
        traceback.print_exc()

def crawl_and_savenext(logtype,param,cparser,queryterm):
    content=getcontent(param)
    cparser(content,queryterm)

def crawl(url,cparser):
    content=getcontent(url)
    cparser(content)

