# Part of https://github.com/haenno/pyIpScanAndWebCrawl

from time import sleep
import socket, ipaddress, threading, random, re
from datetime import datetime, timezone

def get_current_datetime_utc_iso():
    '''Returns string of current UTC date and time in ISO 8601 format.'''
    return str(datetime.now(timezone.utc).isoformat())

def log_new_subnet(new_subent):
    '''Takes string an writes it to log file of scaned subnets.'''
    file_subnets_scaned = "results_subnets.csv"
    doneSubNets = open(file_subnets_scaned,'a')
    doneSubNets.write("\"" + get_current_datetime_utc_iso() + "\";\"" + str(new_subent) +"\"\n")
    doneSubNets.close()

def check_if_subnet_is_fresh(subnet_to_check):
    '''Returns a bool: True=subnet is fresh, False=subnet is scaned'''
    file_subnets_scaned = "results_subnets.csv"
    scaned_subnets = open(file_subnets_scaned,'r')
    for subnet_row in scaned_subnets:
        subnet_from_row = str(re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/24", subnet_row).group())
        if subnet_from_row == subnet_to_check:
            scaned_subnets.close()
            return False
    scaned_subnets.close()        
    return True

def save_open_host(ip,port):
    file_open_www = "results_open_hosts.csv"
    newIps = open(file_open_www,'a')
    newIps.write("\""+get_current_datetime_utc_iso() + "\";\"http://" + str(ip)+":"+str(port)+ "\"\n")
    newIps.close()

def rndSubnet():
    min = 1
    max = 254
    seperator = '.'
    needNewSubnet = True
    rtnStr = ""
    while needNewSubnet:
        tmpSubNet = str(str(int(random.uniform(min,max)))+seperator+str(int(random.uniform(min,max)))+seperator+str(int(random.uniform(min,max)))+seperator+str("0/24"))
        if check_if_subnet_is_fresh(tmpSubNet):
            needNewSubnet = False
            rtnStr = tmpSubNet
    return str(rtnStr)

def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        socket.setdefaulttimeout(2.0) # seconds (float)
        result = sock.connect_ex((ip,port))
        if result == 0:
            save_open_host(ip,port)
        sock.close()
    except:
        pass

while (True):
    scnip = ipaddress.IPv4Network(rndSubnet())
    print ("Scaning " + str(scnip) + "...")
    for ip in scnip: 
        threading.Thread(target=check_port, args=[str(ip), 80]).start()
        sleep(0.1)
        while threading.active_count() > 50 : 
            sleep(1)
    print ("...done.")
    log_new_subnet(scnip)
