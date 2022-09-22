from sys import argv
from os import getpid,kill,remove
from signal import SIGKILL
from time import sleep
from mysql import connector
from util.script import Get_price

SQL_PATH = 'data/sql_login.txt'

def _main():
    args = len(argv)

    try:
        if argv[1]=='start':
            if args==2:
                start()
            elif args==3:
                delay = float(argv[2])
                start(delay)
            elif args==4:
                if argv[3]!='-json':
                    raise IndexError()
                delay = float(argv[2])
                start(delay,False)
        elif argv[1]=='stop':
            if args==2:
                stop()
            else:
                raise IndexError()
    except IndexError as ie:
        print("Syntax error!\nThe command is: python3 scrape.py {[start [delay(h) [-json]]] | stop} \n")
    except ValueError as ve:
        print("Delay must be a number!\n(delay is expressed in hours, default is 1)\n")

def start(delay=1, use_sql=True):
    try:
        if use_sql:
            _loop(delay)
        else:
            print("Error: not implemented yet")
    except FileExistsError:
        print("Error: the script is running.\nTo stop it: python3 scrape.py stop")

def stop():
    try:
        with open('data/pid.txt') as file:
            kill(int(file.readline()),SIGKILL)
        remove('data/pid.txt')

    except FileNotFoundError as fnfe:
        print("Error: the process isn't running or the file 'pid.txt' has been removed",
        "or the script isn't running in the folder 'Prices'.\n",
        "If the file has been removed but the process is still running,",
        "you'll have to kill the process manually with {kill $ID}.",
        "To see a list of the running processes, use {ps -x}.",sep='\n')
    except (ProcessLookupError,ValueError) as fe:
        print("Process not found: the file 'pid.txt' has been modified or is corrupted.",
        "If the process is running, stop it manually with {kill $ID}.",
        "To see a list of the running processes, use {ps -x}.",sep='\n')
        remove('data/pid.txt')

def _loop(delay = 1):
    delay *= 3600  #conversion from hours to seconds

    #registers the pid of the process (to be able to stop it later)
    with open('data/pid.txt', 'x') as file:
        pid = getpid()
        file.write(f'{pid}')
    
    #reads the credentials to log in mysql
    file = open(SQL_PATH, 'r')
    user = file.readline()[:-1]
    pssw = file.readline()[:-1]
    db = file.readline()
    file.close()

    while True:
        mydb = connector.connect(
            host="localhost",
            user=user,
            password=pssw,
            database=db
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT ID,url FROM Items;")
        games = cursor.fetchall()
        for game in games:  #game[0] = ID  game[1] = url
            cursor.execute(f"SELECT price FROM Items WHERE ID={game[0]};")
            old_price = float(cursor.fetchone()[0])
            new_price = Get_price(game[1])
            if old_price!=new_price:
                cursor.execute("UPDATE Items SET price=%.2f,last_change=%.2f WHERE ID=%i;"%(new_price,new_price-old_price,game[0]))
                cursor.execute("INSERT INTO game%i (price) VALUES (%.2f);"%(game[0],new_price))
        mydb.commit()
        cursor.close()
        mydb.close()
        sleep(delay)

if __name__=='__main__':
    _main()