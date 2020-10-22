# pyIpScanAndWebCrawl 
# Copyright (C) 2020 Henning 'haenno' Beier, haenno@web.de, https://github.com/haenno/pyIpScanAndWebCrawl 
# Licensed under the GPLv3: GNU General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.html 
# Here: WIP playgroud


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


url="http://10.200.70.1:80"
#url="http://46.139.86.222/"
#url="http://79.172.214.172:80"
#url="http://61.73.249.110:80"
#url="http://47.240.227.22/"
#url="51.89.120.99:80"
#url="http://80.227.133.226:80"

try:
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver_options = driver.ChromeOptions()
    
    screenshot = driver.save_screenshot('my_screenshot.png')
    driver.quit()        

except Exception as error_message:
    print(" ==> Fehler: \n****************************************\n" + str(error_message) + "\n****************************************")


# Backup for later
'''
from selenium import webdriver
URL = 'http://www.heise.de'
options = webdriver.ChromeOptions()
options.headless = True
#options.add_argument("load-extension=C:/Users/haenno/Nextcloud/BWI/git/pyIpScanAndWebCrawl/idontcareaboutcookies");
#options.add_extension("C:/Users/haenno/Nextcloud/BWI/git/pyIpScanAndWebCrawl/idontcareaboutcookies.crx")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1280,1024) 
driver.get(URL)
#sleep(1.5)
#driver.find_element_by_tag_name('body').screenshot('web_screenshot6.png')
driver.save_screenshot('test.png')
driver.quit()
'''
