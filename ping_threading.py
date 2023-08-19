# -*- coding: UTF-8 -*-
import threading
import subprocess
import re
import time

class ExecutaThread(threading.Thread):

    def __init__(self, host, ip, contador):
        threading.Thread.__init__(self)
        super().__init__()
        self.host = host
        self.ip = ip
        self.contador = contador
		
    def run(self):

        data = [False, None]
 
        try:
            status = subprocess.check_output(['ping', '-c', '3',  '-w10', self.ip])
        except subprocess.CalledProcessError as e:
            status = ''

        if 'packet loss' in str(status):

            pattern = re.compile(r'([0-9]{1,3})% packet loss')
            perda = pattern.search(str(status))[0]

            if '%' in perda:
                perda = perda.split('%')[0].strip()
                perda = int(perda)
                if perda < 34:
                    data = [True, status]
                else:
                    data = [False, None]
            else:
                data = [False, None]
        else:
            data = [False, None]

        if data[0] == True:
            print('OK;'+self.host+';'+self.ip)
        else:
            print('NOK;'+self.host+';'+self.ip)

if __name__ == "__main__":
    # conteúdo list.txt: <ip>;<hostname>
    with open('list.txt') as f:
        lines = f.readlines()
     
n = 6
splited = [lines[i::n] for i in range(n)]

contador = 1
for lista in splited: 
    time.sleep(3)
    for i in lista:
        x = i.split(';')
        ip   = x[0].replace("\n", "")
        host = x[1]
       
        if '.' in ip:
            executaThread = ExecutaThread(host, ip, contador)
            executaThread.start()
            contador = contador + 1
