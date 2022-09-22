import json
from bs4 import BeautifulSoup
import mysql.connector
from re import match

import requests
from util.script import Scrape_cdkeys,Get_price

SAVE_PATH = r'data\url_list.json'
SQL_PATH = 'data/sql_login.txt'

def Save(url):
	valid_link = match('http', url)!=None
	if not(valid_link): return 'Link not valid :('
	
	domain_name = url[8:]
	if match('www.', domain_name)!=None: domain_name = domain_name[4:]
	domain_name = domain_name[:domain_name.find('/')]

	with open(SAVE_PATH) as file:
		dict = json.load(file)
	found = _Search_correspondence(domain_name, dict['domain'], 'name')
	
	if found>=0:
		if _Search_correspondence(url, dict['domain'][found]['item'], 'url')>=0:
			return 'link already exists in memory :|'
		else:
			name = input("Write a name to identify it in the future: ")
			dict['domain'][found]['item'].append({'identifier':name, 'url':url})
			Load(dict)
			return 'link successfully added :)'
	else:
		name = input("Write a name to identify it in the future: ")	
		dict['domain'].append({'name': domain_name, 'item': [{'identifier': name, 'url': url}]})
		Load(dict)
		
		return 'link successfully added :)'

def SaveSQL(url, name=''):
	# basic url validity check
	valid_link = match('http[s]://', url)!=None
	if not(valid_link): return "link not valid, *have you pasted the entire url?*"
	# read mysql credentials from local file
	file = open(SQL_PATH, 'r')
	user = file.readline()[:-1]
	pssw = file.readline()[:-1]
	db = file.readline()
	file.close()
	# access to the database
	mydb = mysql.connector.connect(
		host="localhost",
		user=user,
		password=pssw,
		database=db
	)
	# initialize cursor
	cursor = mydb.cursor()
	# find site domain
	domain = url[8:]
	if match('www.', domain)!=None: domain = domain[4:]
	domain = domain[:domain.find('/')]

	if domain=='cdkeys.com':
		# scrape data
		game_data = Scrape_cdkeys(url)
		cursor.execute(f"SELECT url FROM Items WHERE url='{game_data['url']}';")
		# duplicate url check
		if cursor.fetchone()!=None:
			cursor.close()
			mydb.close()
			return "Item already in database!"

		if name=='': name = game_data['title']
		else: game_data['title'] = name
		# insert item to the list
		query = ("INSERT INTO Items (domain,title,url,price,currency,image,last_change) "
				"VALUES (%(domain)s,%(title)s,%(url)s,%(price)s,%(currency)s,%(image)s,0.00)")
		cursor.execute(query,game_data)
		# create table for prices history
		cursor.execute("SELECT ID FROM Items WHERE url='%s';"%game_data['url'])
		ID = cursor.fetchone()[0]
		cursor.execute(f"CREATE TABLE IF NOT EXISTS game{ID} "
			"(price DECIMAL(10,2) NOT NULL, date DATETIME DEFAULT(CURRENT_TIMESTAMP) PRIMARY KEY);")
		cursor.execute("INSERT INTO game%s (price) VALUES (%f);"%(ID,game_data['price']))
	else:
		# duplicate url check
		cursor.execute(f"SELECT url FROM Items WHERE url LIKE '{url}%';")
		if cursor.fetchone()==None:
			# scrape title and price
			price = Get_price(url)
			if name=='': name = get_name(url)
			cursor.execute("INSERT INTO Items (domain,name,url,price,last_change) VALUES (%s,%s,%s,%f,0.00);",(name,url,domain,price))
			cursor.execute("SELECT ID FROM Items WHERE url='%s';"%url)
			ID = cursor.fetchone()[0]
			cursor.execute(f"CREATE TABLE IF NOT EXISTS {ID}"
				"(price DECIMAL(10,2) NOT NULL, date DATETIME DEFAULT(CURRENT_TIMESTAMP) PRIMARY KEY);")
		else:
			cursor.close()
			mydb.close()
			return f"Item already in database!"
	mydb.commit()
	cursor.close()
	mydb.close()
	return f"{name} successfully added to database!"

def _Search_correspondence(tofind, list, key):
	for i in range(0, len(list)):
		if list[i][key]==tofind: return i
	return -1

def Load(dict):
	with open(SAVE_PATH, 'w') as file:
		json.dump(dict, file)

def get_name(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	return soup.title