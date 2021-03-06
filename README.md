## pyIpScanAndWebCrawl 
Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
**Here: Readme**

### About 
Python scripts to scan random IP addresses for open and running web servers. If found it collects some details on them for later scientific evaluation. This without any manipulation of or input to the website or web server. This results in a collection of publicly accessible and viewable data of information open at anytime to anyone about websites and web servers.

### TLDR:
**Top left:** Script that scans all IP addresses from random subenets.

**Top right:** Scrips that takes screenshots from IPs with running webservers.

**Bottom:** As the result, the screenshots.

![GIF of the scripts running](/project_running.gif "GIF of the scripts running")


### Ideas
 - Connect the containers with APIs (REST?)
 - Find good or common style and naming conventions and refactor accordingly
 - Implement a website to interface to the collected data (filters, sorting, previews, ...)
 - Implement running the different tasks (scanning, collecting data, making screenshots) as a service, the services then start- and stoppable over the web interface

### Changelog

2020-11-11: 
 - WIP: Set up docker environment (Create containers with the scrips as microservices)

2020-11-04: 
 - Update of readme.
 - Added ideas.

2020-10-24:
 - Replace storage in files with a database of some kind
 - Changed screenshot function: Running on its own, outside of scan function. 

2020-10-22: 
 - Implement collection of HTTP headers 
 - Implement taking screenshots of the open web servers  

### Todo
 - Check back and work again on screenshots with chromedriver (loading extensions, threading)

### FAQ
 - The chromedriver.exe (or accordingly) needs to be in the directory of the scan script. It's not included here. The binary can be obtained directly from google.

### Credit to
 - Pedro Lobito for 'a fast multi-threaded port scanner' from https://stackoverflow.com/a/55663026 (License https://creativecommons.org/licenses/by-sa/4.0/ CC BY-SA 4.0) 
 - Klaidonis for 'headless selenium' from https://stackoverflow.com/a/57338909 (License https://creativecommons.org/licenses/by-sa/4.0/ CC BY-SA 4.0) 