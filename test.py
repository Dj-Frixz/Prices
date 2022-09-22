import os
print(os.path.dirname(os.path.abspath(__file__)))

with open(r'data\sql_login.txt', 'r') as file:
    user = file.readline()[:-1]
    pssw = file.readline()
    print(user,pssw,end='',sep='\n')