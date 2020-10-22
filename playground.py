# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: WIP playgroud

import requests
from requests.api import request

#url="http://10.200.70.1"
#url="http://46.139.86.222/"
#url="http://79.172.214.172:80"
#url="http://61.73.249.110:80"
#url="http://47.240.227.22/"
url="http://51.89.120.99:80"

try:
    request_result = requests.get(url)

    #print(request_result.text) #100 Zeichen? 100 Zeilen?
    #print(request_result.content)
    #print(request_result.status_code) # 1
    #print(request_result.headers) # 2
    #print(request_result.cookies) # egal
    #print(request_result.json) 

    if int(request_result.status_code == 200):
        print("HTTP Status: 200 OK")
        print("HTTP Headers: \n    " + str(request_result.headers))
        print("HTTP Text-Content: \n   ")
        #tmptxt2=request_result.text.splitlines()
        print(request_result.text[:1000])
        '''
        for zeile in request_result.text.splitlines():
            print(zeile)
            tmptxt=tmptxt+"\n"+zeile
            print (str(len(tmptxt)))
        '''
    else:
        print("HTTP Status:" + str(request_result.status_code))
        
except Exception as error_message:
    print(" ==> Fehler: \n****************************************\n" + str(error_message) + "\n****************************************")