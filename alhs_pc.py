from asyncio.windows_events import NULL
from cgitb import html
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
import csv
file = open('list_20220918.csv', 'a+', encoding='utf-8', newline='')
csv_writer = csv.writer(file)
for page_i in range(0,300):
    print(page_i)
    url='https://alhs.xyz/index.php/page/'+str(page_i)+'/'
    if page_i==1:
        url='https://alhs.xyz/'
    headers={
        ':authority':'alhs.xyz',
        ':method':'GET',
        ':path':'/' if page_i==1 else '/index.php/page/'+str(page_i)+'/',
        ':scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'cookie':'_ga=GA1.1.1154740192.1662957518; argon_user_token=ae4870684b33fcdd90368f6d9b710c1c; PHPSESSID=b1cf3a174e646786ef7f6234880089b0; pvc_visits[0]=1663044309b135; _ga_41JP6N6C2D=GS1.1.1662960885.2.1.1662960886.59.0.0; __cf_bm=Vd6FB4XK1nynM1KoS1dtZKwIEsMvwGEC8CwNcLAKaEk-1662960889-0-ASaW64EROIkrRk2FqjwOh5dABsqBzqFg42riuH5pLVf6iz9VBQTlVI+Bifh9GkNDvIWNgupuQbIAaAQKdoWJXgmx7IyhZNKtk405UH4kE1Z2sL7dqmAi8jUVJgoRdyX1zA==',
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
    response = sessions.post(url, headers=headers,timeout=30)
    html=response.text
    soup = BeautifulSoup(html,'lxml')
    item=soup.find(id='main')
    for i in item:
        title=NULL
        href=NULL
        author=NULL
        fa_time=NULL
        bq=NULL
        tags=NULL
        j=BeautifulSoup(str(i),'lxml')
        content=j.find(attrs={'class':'post-title'})
        if content == None:
            continue
        title=content.text
        href=content['href']
        content=j.find(attrs={'class':'post-meta-detail post-meta-detail-author'})
        if content != None:
            author=content.text
        content=j.find(attrs={'class':'post-meta-detail post-meta-detail-time'})
        if content != None:
            fa_time=content.text
        content=j.find(attrs={'class':'post-meta-detail post-meta-detail-categories'})
        if content != None:
            bq=content.text
        content=j.findAll(attrs={'class':'tag badge badge-secondary post-meta-detail-tag'})
        if content!=None:
            tags=[t.text for t in content]
        csv_writer.writerow([
            title.replace("\t","").replace("\r","").replace("\t",""),
            href.replace("\t","").replace("\r","").replace("\t",""),
            author.replace("\t","").replace("\r","").replace("\t",""),
            fa_time.replace("\t","").replace("\r","").replace("\t",""),
            bq.replace("\t","").replace("\r","").replace("\t",""),
            tags
        ])
file.close()
    
'''
# from selenium.webdriver.common.by import By

# # 导入selenium的浏览器驱动接口
# from selenium import webdriver

# # 要想调用键盘按键操作需要引入keys包
# from selenium.webdriver.common.keys import Keys

# # 导入chrome选项
# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome(options=options)
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
# })
# driver.get("https://alhs.xyz/index.php/page/2/")
# time.sleep(5)
# html = driver.execute_script("return document.documentElement.outerHTML")
# print(html)
# with open('test.html','w',encoding='utf-8') as f:
#    f.write(html)
# driver.quit()
'''