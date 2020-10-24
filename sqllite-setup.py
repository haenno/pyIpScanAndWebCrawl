# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: Script for creating tables (run only once or when realy needed)

import sqlite3
import myconstants as conf

db_connection = sqlite3.connect(conf.SQLITE_DB_FILE)
db = db_connection.cursor()

# Empty DB (only if you know that you realy want to)
'''
db.execute("DROP TABLE scanned_subnets;")
db.execute("DROP TABLE open_hosts;")
db.execute("DROP TABLE screenshots;")
'''

# Create tables
#'''
db.execute("CREATE TABLE scanned_subnets (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime DATETIME NOT NULL, subnet VARCHAR(18) NOT NULL);")
db.execute("CREATE TABLE open_hosts (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime DATETIME NOT NULL, ip VARCHAR(15) NOT NULL, port VARCHAR(7) NOT NULL, url VARCHAR(30) NOT NULL, http_status_code INTEGER NOT NULL, http_headers TEXT, html_probe TEXT);")
db.execute("CREATE TABLE screenshots (id INTEGER PRIMARY KEY AUTOINCREMENT, open_hosts_id INTEGER NOT NULL, datetime DATETIME NOT NULL, used_url VARCHAR(30) NOT NULL, filename VARCHAR(50) NOT NULL);")
#'''

# Insert some example data
#'''
db.execute("INSERT INTO scanned_subnets (datetime, subnet) VALUES (CURRENT_TIMESTAMP,'127.0.0.0/24');")
db.execute("INSERT INTO open_hosts (datetime, ip, port, url, http_status_code, http_headers, html_probe) VALUES (CURRENT_TIMESTAMP,'127.0.0.1','80','http://127.0.0.1:80',200,'example data http headers','example data html probe');")
db.execute("INSERT INTO screenshots (open_hosts_id, datetime, used_url, filename) VALUES (1, CURRENT_TIMESTAMP,'http://127.0.0.1:80','nonexistant.png');")
#'''

db_connection.commit()
db.close
