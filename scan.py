# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: Script for finding open hosts and saving them

from time import sleep
from datetime import datetime, timezone
import socket
import ipaddress
import threading
import random
import re
import requests

def get_current_datetime_utc_iso():
    '''Gets the current UTC date and time in ISO 8601 format.
    Returns this timestamp as a string.'''
    return str(datetime.now(timezone.utc).isoformat())

def log_new_subnet(new_subent):
    '''Takes string an writes it to log file of sacnned subnets. 
    Returns nothing.'''
    file_subnets_sacnned = "results_subnets.csv"
    doneSubNets = open(file_subnets_sacnned,'a')
    doneSubNets.write(get_current_datetime_utc_iso() + "," + str(new_subent) +"\n")
    doneSubNets.close()

def check_if_subnet_is_fresh(subnet_to_check):
    '''Takes a subnet as a string and checks it against a list of already sacnned subnets.
    Returns a bool: True=subnet is fresh, False=subnet is sacnned'''
    file_subnets_sacnned = "results_subnets.csv"
    scanned_subnets = open(file_subnets_sacnned,'r')
    for subnet_row in scanned_subnets:
        subnet_from_row = str(re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/24", subnet_row).group())
        if subnet_from_row == subnet_to_check:
            scanned_subnets.close()
            return False
    scanned_subnets.close()        
    return True

def save_open_host(ip, port, http_status_code, http_header, html_probe):
    '''Takes (IP, port, HTTP status code, HTTP header) and writes it all to a list of open hosts for later usage. 
    Returns nothing.'''
    file_open_hosts = "results_open_hosts.csv"
    open_hosts = open(file_open_hosts,'a')
    open_hosts.write(get_current_datetime_utc_iso() + ",http://" + str(ip)+":"+str(port)+","+str(http_status_code)+",\""+ http_header +"\",\"" + html_probe + "\"\n")
    open_hosts.close()

def get_random_new_subnet():
    '''Creates a random subnet until it finds a not already scanned one. 
    Returns the new subnet as a string.'''
    need_new_subnet = True
    subnet_to_return = ""
    while need_new_subnet:
        tmp_subnet = str(str(int(random.uniform(1,254)))+'.'+str(int(random.uniform(1,254)))+'.'+str(int(random.uniform(1,254)))+'.'+str("0/24"))
        if check_if_subnet_is_fresh(tmp_subnet):
            need_new_subnet = False
            subnet_to_return = tmp_subnet
    return str(subnet_to_return)

def check_ip(ip, port):
    '''Takes an IP and port, tries to connect, if succeed it collects HTTP headers and writes them and the host information (IP and port) to the list of open hosts.
    Returns nothing.'''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        socket.setdefaulttimeout(2.0) # seconds (float)
        result = sock.connect_ex((ip,port))
        if result == 0:
            print(" > found one: http://"+str(ip)+":"+str(port))
            sleep(0.5)
            http_headers = get_http_headers("http://"+str(ip)+":"+str(port))
            save_open_host(ip, port, http_headers[0], http_headers[1], http_headers[2])
        sock.close()
    except:
        pass

def get_http_headers(url):
    '''Takes a URL as a string and tries to get HTTP status codes and headers and the frist 2000 characters of the HTML. 
    Returns: HTTP status code as int, HTTP header as a string, HTML content as string.'''
    try:
        request_result = requests.get(url)
        http_header = str(request_result.headers)
        http_status_code = request_result.status_code
        html_probe = request_result.text[:2000]
    except Exception as error_message:
        http_header = str(error_message)
        http_status_code= 999
        html_probe = ""
    # replacing here only for saving in csv file, later to change when database is used    
    return http_status_code, http_header.replace("\"", "'").replace(",", ";").replace("\n", " ").replace("\r", " "), html_probe.replace("\"", "'").replace(",", ";").replace("\n", " ").replace("\r", " ")

while (True):
    subnet_to_scan = ipaddress.IPv4Network(get_random_new_subnet())
    print ("Scaning " + str(subnet_to_scan) + "...")
    for ip in subnet_to_scan: 
        threading.Thread(target=check_ip, args=[str(ip), 80]).start()
        sleep(0.05)
        while threading.active_count() > 50: 
            sleep(1)
    print ("...done.")
    log_new_subnet(subnet_to_scan)
