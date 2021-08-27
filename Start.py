from os import system, get_terminal_size, write

while(True):
    text_offset = int((get_terminal_size()[0]-48)/2)
    from util.menu import options
    system('COLOR 0E')
    print('Welcome to the\n\n\n')
    print(' '*text_offset+'                                     _')
    print(' '*text_offset+'          . . .  ——— . .  .  ^  ——— /_')
    print(' '*text_offset+'          |_| |_  |  | |\/| /^\  |  \_')
    print(' '*text_offset+'                  PRICE SCRAPER!\n\n\n\n\n\n\n')
    print('Choose an option:\n')
    print(' '*text_offset+'0 - Choose url from list     1 - Add new url')
    print(' '*text_offset+'2 - Look at the url tree     3 - Modify the url list')
    print(' '*text_offset+'4 - 5 - quit );')
    print('\n\n\n\n')

    n = int(input())
    if n<0 or n>=len(options):
        from time import sleep
        from sys import stdout
        system('cls && color 4e')
        message = 'So... you actually thought you could trick me like that?      Dumb move human'
        print(message)
        #for x in range(0,6):
        #    sleep(0.5)
        #    stdout.write(message[x])
        #sleep(3)
        #for x in range(6,len(message)):
        #    sleep(0.1)
        #    stdout.write(message[x])
        print('\n\n\n\n\n')
        system('pause & cls')
    else:
        lambda: system('cls')
        options[n]()