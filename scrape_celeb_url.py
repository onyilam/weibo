import time            
import re, os, sys, codecs            
import shutil
import urllib 
import pandas as pd
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



def isElementPresent(locator):
    """
    This function checks if the xpath element is in the page
    """
    try:
        driver.find_element_by_xpath(locator)
    except NoSuchElementException:
        return False
    return True
    

def GetWeiboUrl(name):
    """
    This function takes the name of the celebrity and search for the verified weibo account of the celeb
    """
    
    searchurl = 'http://s.weibo.com/weibo/' + name
    driver.get(searchurl)
    time.sleep(3)
    isExist = isElementPresent('//*[@id="pl_weibo_directtop"]/div/div/div/div[2]/p[1]/a[2]')
    if isExist is True:
        url = driver.find_element_by_xpath('//*[@id="pl_weibo_directtop"]/div/div/div/div[2]/p[2]/a').text
    else:
        url = 'No weibo account'
        
    #close tab
    driver.execute_script("window.close('');") 
    driver.switch_to_window(driver.window_handles[0])
    driver.close()
    return(url)

         
for name in celeb_list:
    successful = False
    while not successful:
        try:
            driver = webdriver.Chrome('/Users/onyi/Dropbox/weibo/chromedriver')
            driver.set_page_load_timeout(45)
            wait = ui.WebDriverWait(driver,5)
            url=GetWeiboUrl(name)
            successful = True
        except TimeoutException:
            successful = False
            driver.close()
        except NoSuchElementException:
            successful =False
            driver.close()
    
    print(name, url)
    urlfile = codecs.open("WeiboUrl.txt", 'a', 'utf-8')
    urlfile.write('=====================================================================\r\n')
    urlfile.write(u'Name: ' + name  + '\r\n')
    urlfile.write(u'url: ' + url  + '\r\n')
    urlfile.close()