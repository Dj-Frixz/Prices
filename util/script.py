import requests
from re import search
from random import choice
from bs4 import BeautifulSoup
from util.headers import headers, user_agent_list
#import csv

def Get_price(url):
    save_path = r"data\prices_history.csv"
    domain = url[:url[8:].find('/')+1]
    headers[0]['referer'] = domain
    headers[1]['authority'] = domain
    #proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
    #proxies = {'https': choice(proxies_list)}
    pos = -1
    if domain[8:domain[8:].find('/')] != 'amazon':
        headers[0]['user-agent'] = choice(user_agent_list)
        page = requests.get(url, headers=headers[0])#, proxies=proxies)
        pos = page.text.find('price:')
        if pos==-1:
            pos = page.text.find('price"')
    if page.status_code!=200 or pos==-1:
        headers[1]['user-agent'] = choice(user_agent_list)
        page = requests.get(url, headers=headers[1])
        pos = page.text.find('price:')
        if pos==-1:
            pos = page.text.find('price"')
    price = search(r'\d+[.,]\d{2}', page.text[pos:])[0]
    #prices = []
    #prices.append(price)

    #with open(save_path, 'w', newline='') as file:
    #        writer=csv.writer(file)
    #        writer.writerow(prices)
    return float(price)

def Get_price_cdkeys(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    return float(soup.find(property="product:price:amount")['content'])

def Scrape_cdkeys(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    game = {
        'domain':'cdkeys.com',
        'title':soup.find(property="og:title")['content'],
        'url':soup.find(property="og:url")['content'],
        'price':float(soup.find(property="product:price:amount")['content']),
        'currency':soup.find(property="product:price:currency")['content'],
        'image':soup.find(property="og:image")['content']
    }
    return game