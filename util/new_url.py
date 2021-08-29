import json

SAVE_PATH = r'data\url_list.json'

def Save(url):
	from re import match
	valid_link = match('http', url)!=None
	if not(valid_link): return 'Link not valid :('
	
	domain_name = url[8:]
	if match('www.', domain_name)!=None: domain_name = domain_name[4:]
	domain_name = domain_name[:domain_name.find('/')]
	
	with open(SAVE_PATH) as file:
		dict = json.load(file)
	
	found = Search_correspondence(domain_name, dict['domain'], 'name')
	if found>=0:
		if Search_correspondence(url, dict['domain'][found]['item'], 'url')>=0:
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

def Search_correspondence(tofind, list, key):
	for i in range(0, len(list)):
		if list[i][key]==tofind: return i
	
	return -1

def Load(dict):
	with open(SAVE_PATH, 'w') as file:
		json.dump(dict, file)
