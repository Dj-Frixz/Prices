from util.new_url import SaveSQL
from sys import argv

if __name__=='__main__':

    args = len(argv)

    #try:
    if args==2:
        print(SaveSQL(argv[1]))
    elif args==3:
        print(SaveSQL(argv[2],argv[1]))
    else:
        raise SyntaxError()
    #except:
    #    print('Error: invalid args or invalid url!\nValid syntax is: python3 add-url.py [name] url\n*Does your url start with "https://"?*')