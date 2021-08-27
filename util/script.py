from requests import get
from re import search
from random import choice
import csv

def Get_price(url):
    save_path = r"data\prices_history.csv"
    domain = url[:url[8:].find('/')+1]
    headers = [
        {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': '',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': domain,
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        },
        {
            'authority': domain,
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': '',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    ]
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    ]
    #proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
    #proxies = {'https': choice(proxies_list)}
    pos = -1
    if domain[8:domain[8:].find('/')] != 'amazon':
        page = get(url, headers=headers[0])#, proxies=proxies)
        pos = page.text.find('price:')
        if pos==-1:
            pos = page.text.find('price"')
    if page.status_code!=200 or pos==-1:
        page = get(url, headers=headers[1])
        pos = page.text.find('price:')
        if pos==-1:
            pos = page.text.find('price"')
    price = search(r'\d+[.,]\d{2}', page.text[pos:])[0]
    prices = []
    prices.append(price)

    with open(save_path, 'w', newline='') as file:
            writer=csv.writer(file)
            writer.writerow(prices)
    return price
