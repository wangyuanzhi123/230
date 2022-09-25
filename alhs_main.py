from asyncio.windows_events import NULL
from asyncore import read
from cgitb import html
import csv
from time import sleep, time
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
def get_one(url):
    url='https://alhs.xyz'+url
    headers={
        ':authority':'alhs.xyz',
        ':method':'GET',
        ':scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'sec-ch-ua':'"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'Windows"',
        'sec-fetch-dest':'document',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    sessions = requests.session()			
    sessions.mount(url, HTTP20Adapter())
    proxies={ 
    'http':'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890'
    }	
    #proxies=proxies
    response = sessions.get(url,headers=headers,timeout=(50, 60))
    html=response.text
    soup=BeautifulSoup(html,'lxml')
    s_list=[]
    try:
        list=soup.find(attrs={'class':'post-series-list'}).findChildren('li')
        for i in list:
            href='this'
            a=i.findChild('a')
            if a!=None:
                href=a['href'].replace('https://alhs.xyz','')
                s_list.append({href:i.text})
    except:
        pass
    post_content=''
    try:
        content=soup.find(attrs={'class':'post-content'})
        post_content=str(content)
    except:
        pass
    try:
        for i in content.findAll(attrs={'class':'post-series-list'}):
            i.decompose()
        for i in content.findAll('toc'):
            i.decompose()
        for i in content.findAll(attrs={'class':'saboxplugin-wrap'}):
            i.decompose()
        for i in content.findAll(id='related_posts'):
            i.decompose()
        for i in content.findAll(attrs={'class':'wpulike wpulike-voters  wpulike-is-pro'}):
            i.decompose()
        for i in content.findAll(attrs={'class':'post-series'}):
            i.decompose()
    except:
        pass
    text=''
    try:
        text=content.text.replace('[友情推广，备注艾利浩斯图书馆有优惠哦]','').replace('这个页面/文章内容有问题？点这里反馈/举报。','')
    except:
        pass
    return post_content,text,s_list
file = open('list.csv', 'r+', encoding='utf-8', newline='')
csv_read = csv.reader(file)
file2 = open('new_list.csv', 'a+', encoding='utf-8', newline='')
csv_write = csv.writer(file2)
num=0
sleep(1)
for row in csv_read:
    try:
        print('\n'+str(num),end="")
        num=num+1
        if num<583:
            continue
        post_content=''
        text=''
        s_list=''
        for i in range(0,30):
            print('.',end="")
            try:
                post_content,text,s_list=get_one(row[1].replace('https://alhs.xyz',''))
                break
            except Exception as e:
                sleep(1)
        row.append(s_list)
        row.append(text)
        row.append(post_content)
        csv_write.writerow(row)
        f=open('alhs_txt/'+row[0]+'.txt','w', encoding='utf-8')
        f.write(text)
        f.close()
        f=open('alhs_html/'+row[0]+'.html','w', encoding='utf-8')
        f.write(post_content)
        f.close()
    except Exception as e:
        print(row)
        print(e)
