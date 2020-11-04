# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: Script for creating screenshots

from selenium import webdriver
from myfunctions import sqldb_query, sqldb_execute_bindings, handle_error, write_to_console
from datetime import datetime, timezone
from time import sleep, time
import threading

def make_screenshot(url, host_id):
    '''Takes a URL and tries to make a screenshot and saves it if successful under a mostly random filename.
    Returns filename of screenshot as string.'''
    # Chromedriver seems to have a very poor documentation. Not all functions are working as expected. Here only with most basic functions. Not able to let it run realy silent.
    try:
        write_to_console(" > Starting headless chrome for '"+str(threading.current_thread().getName())+"'")
        options = webdriver.ChromeOptions()
        #options.add_argument("load-extension=C:/Users/haenno/Nextcloud/BWI/git/pyIpScanAndWebCrawl/idontcareaboutcookies");    
        #options.add_extension("C:/Users/haenno/Nextcloud/BWI/git/pyIpScanAndWebCrawl/idontcareaboutcookies.crx")
        #options.headless = True
        options.add_argument("--silent")
        options.add_argument("--headless")
        options.add_argument("--log-level=OFF")    
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280,1024) 
        driver.get(url)
        sleep(0.5)
        filename = ((str(get_current_datetime_utc_iso())+str(url)).replace(":","-").replace("/","-").replace(".","-"))+".png"
        if driver.save_screenshot("screenshots/"+filename):
            sqldb_execute_bindings("INSERT INTO screenshots (open_hosts_id, datetime, used_url, filename) VALUES (?, CURRENT_TIMESTAMP,?,?);",(host_id, url, filename))
            write_to_console(" > Screenshot taken from '"+str(threading.current_thread().getName())+"', filename '" + filename + "'")
        else:
            sqldb_execute_bindings("INSERT INTO screenshots (open_hosts_id, datetime, used_url, filename) VALUES (?, CURRENT_TIMESTAMP,?,?);",(host_id, url, "dummy.png"))
            write_to_console(" > No screenshot taken from '"+str(threading.current_thread().getName())+"', wrote 'dummy.png' to DB")
        driver.quit()
    except Exception as error_message:
        handle_error(error_message)

def get_current_datetime_utc_iso():
    '''Gets the current UTC date and time in ISO 8601 format.
    Returns this timestamp as a string.'''
    return str(datetime.now(timezone.utc).isoformat())

def loop_screenshots():
    '''Starts 10 headless chrome browser and tries to makes a screenshot of open hosts with HTTP status code 200.
    Returns string "ok" if all threads ended in time, returns string "timeout" if timelimit is hit.'''
    loop_timeout = time() + 90
    write_to_console("Starting new batch of screenshots to make...")
    workload = sqldb_query("SELECT open_hosts.id as oh_id, open_hosts.url as url FROM open_hosts WHERE open_hosts.id NOT IN (SELECT open_hosts_id FROM screenshots) AND open_hosts.http_status_code = 200 ORDER BY open_hosts.datetime DESC LIMIT 15;")
    for result in workload:
        threading.Thread(name=str(result[1]), target=make_screenshot, args=[str(result[1]), str(result[0])]).start()
        sleep(0.5)
    while threading.active_count() != 1: 
        write_to_console(" > Remaing screenshots to take: "+ str(threading.active_count()-1))
        sleep(1.5)     
        if time() > loop_timeout:
            write_to_console("...Timelimit hit, starting next batch.")
            return "timeout"
    write_to_console("...batch done.")
    return "ok"
    
while True:
    try:
        loop_screenshots()
    except Exception as error_message:
        handle_error(error_message)
