# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: Script for finding open hosts and saving them

from time import sleep
from myfunctions import sqldb_execute, sqldb_query, sqldb_execute_bindings, handle_error, write_to_console
import socket
import ipaddress
import threading
import random
import requests

def log_new_subnet(new_subnet):
    '''Takes string an writes it to the DB table of scanned subnets. 
    Returns nothing.'''
    sqldb_execute("INSERT INTO scanned_subnets (datetime, subnet) VALUES (CURRENT_TIMESTAMP,'"+str(new_subnet)+"');")    

def check_if_subnet_is_fresh(subnet_to_check):
    '''Takes a subnet as a string and checks it against the DB table of already sacnned subnets.
    Returns a bool: True=subnet is fresh, False=subnet is sacnned'''
    scanned_subnets = sqldb_query("SELECT subnet FROM scanned_subnets WHERE subnet = '"+str(subnet_to_check)+"';")
    if len(scanned_subnets) == 0:
        return True
    else:
        return False

def save_open_host(ip, port, url, http_status_code, http_header, html_probe):
    '''Takes (IP, port, HTTP status code, HTTP header) and writes it all to the DB table of open hosts for later usage. 
    Returns nothing.'''
    try:
        sqldb_execute_bindings("INSERT INTO open_hosts (datetime, ip, port, url, http_status_code, http_headers, html_probe) VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?);", (ip,port,url,http_status_code,http_header,html_probe))
    except Exception as error_message:
        handle_error(error_message)

def get_random_new_subnet():
    '''Creates a random subnet until it finds a not already scanned one. 
    Returns the new subnet as a string.'''
    need_new_subnet = True
    subnet_to_return = ""
    while need_new_subnet:
        tmp_subnet = str(int(random.uniform(1,254)))+'.'+str(int(random.uniform(0,255)))+'.'+str(int(random.uniform(0,255)))+'.'+"0/24"
        if check_if_subnet_is_fresh(tmp_subnet):
            need_new_subnet = False
            subnet_to_return = tmp_subnet
    return subnet_to_return

def check_ip(ip, port):
    '''Takes an IP and port, tries to connect, if succeed it collects HTTP headers and HTML probe, then writes the data and the host information (IP and port) to the list of open hosts.
    Returns nothing.'''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        socket.setdefaulttimeout(5.0) # seconds (float)
        result = sock.connect_ex((ip,port))
        if result == 0:
            url= "http://"+str(ip)+":"+str(port)
            http_headers = get_http_headers(url)
            save_open_host(ip, port, url, http_headers[0], http_headers[1], http_headers[2])            
            write_to_console(" > Found one: " + url)
        sock.close()
    except Exception as error_message:
        handle_error(error_message)

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
    return http_status_code, http_header, html_probe

while (True):
    subnet_to_scan = ipaddress.IPv4Network(get_random_new_subnet())
    write_to_console("Scaning " + str(subnet_to_scan) + "...")
    for ip in subnet_to_scan.hosts(): 
        threading.Thread(target=check_ip, args=[str(ip), 80]).start()
        #sleep(0.05)
    while threading.active_count() != 1: 
        write_to_console(" > Remaing IPs to scan: "+ str(threading.active_count()-1))
        sleep(1.5)        
    write_to_console("...done.")
    log_new_subnet(subnet_to_scan)
