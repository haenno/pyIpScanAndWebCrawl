# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: Functions for use in multiple files

import sqlite3
import myconstants as conf
from time import sleep

def sqldb_execute(sql_query_string):
    '''Takes an SQL query as a string an sends it so the database. For use with SQL querys without return of data.
    Returns noting. '''
    db_connection = sqlite3.connect(conf.SQLITE_DB_FILE)
    db = db_connection.cursor()
    db.execute(str(sql_query_string))
    db_connection.commit()
    db.close

def sqldb_execute_bindings(sql_query_string, bindings):
    '''Takes an SQL query as a string and a list of bindings and sends them to the database. For use with SQL querys without return of data.
    Returns noting. '''
    try:
        db_connection = sqlite3.connect(conf.SQLITE_DB_FILE)
        db = db_connection.cursor()
        db.execute(str(sql_query_string), bindings)
        db_connection.commit()
        db.close
    except Exception as error_message:
        handle_error(error_message)

def sqldb_query(sql_query_string):
    '''Takes an SQL query as a string an sends it so the database. For use with SQL querys without return of data.
    Returns noting. '''    
    db_connection = sqlite3.connect(conf.SQLITE_DB_FILE)
    db = db_connection.cursor()
    db.execute(str(sql_query_string))
    query_result = db.fetchall()
    db.close
    return query_result

def handle_error(error_message):
    '''Takes an error message and prints it out as a string.
    Returns nothing.'''
    # Todo: Think about logging.
    print(" ==> ERROR: '"+str(error_message).replace("\n"," ").replace("\r"," ")+"'")
    sleep(0.25)

def write_to_console(message):
    '''Takes a message as a string and writes it to the console.
    Returns noting.'''
    # Todo: Find out why sometimes the output is without a new line. 
    print(str(message).rstrip())
    sleep(0.25)