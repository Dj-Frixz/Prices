from util.script import Get_price
from util.new_url import Save
import json
from os import system
clear = lambda: system('cls')
pause = lambda: system('pause')

with open(r'data\url_list.json') as file:
        dict = json.load(file)

def show_price():
    choice = choose()
    if choice!=None:
        price = Get_price(choice)
        system('COLOR 0C')
        print(f'\n   {price}\n\n\n')
        pause()
    clear()

def insert_url():
    clear()
    url = input('Paste the url you want to add:\n')
    print('\n\n\n\n')
    Save(url)
    pause()
    clear()

def gen_url_tree():
    x = len(dict['domain'])
    if x==0:
        clear()
        print('\n   Oh no, you have 0 urls saved!\nStart by adding one...\n')
        pause()
        clear()
    else:
        clear()
        for i in range(0,x):
            domain_name = dict['domain'][i]['name']
            y = len(dict['domain'][i]['item'])
            stamp = f'\n - {domain_name}  '
            print(stamp, end='')
            for l in range(0,y):
                url_name = dict['domain'][i]['item'][l]['identifier']
                if l==0: print(f'— {url_name}')
                else: print(' '*len(stamp),f'∟ {url_name}')
        print('\n\n')
        pause()
        clear()

def delete_url():
    clear()
    if len(dict['domain'])==0:
        print('\n   Oh no, you have 0 urls saved!\nStart by adding one...\n')
        pause()
        clear()
        return None
    else:
        choose_domain()
        dom_num = int(input())
        clear()
        choose_url(dict['domain'][dom_num]['item'])
        item_num = int(input())
        clear()
        erased_url = dict['domain'][dom_num]['item'][item_num]['identifier']
        dict['domain'][dom_num]['item'].pop(item_num)
        with open(r'data\url_list.json', 'w') as file:
            json.dump(dict, file)
        print(f'{erased_url} deleted correctly! What was wrong with this one? :(\n\n')
        pause()
        clear()

def choose():
    clear()
    print('Choose a domain:\n')
    if len(dict['domain'])==0:
        clear()
        print('\n   Oh no, you have 0 urls saved!\nStart by adding one...\n')
        pause()
        clear()
        return None
    else:
        choose_domain()
        dom_num = int(input())
        clear()
        choose_url(dict['domain'][dom_num]['item'])
        item_num = int(input())
        clear()
        return dict['domain'][dom_num]['item'][item_num]['url']

def choose_domain():
    n = len(dict['domain'])
    for i in range(0,n):
        name = dict['domain'][i]['name']
        print(f'{i} - {name}')
    print('\n\n')
    return

def choose_url(list):
    print('Choose an item:\n')
    n = len(list)
    for i in range(0,n):
        name = list[i]['identifier']
        print(f'{i} - {name}')
    print('\n\n')



options = {
    0 : show_price,
    1 : insert_url,
    2 : gen_url_tree,
    3 : delete_url,
    4 : lambda: quit()
}
