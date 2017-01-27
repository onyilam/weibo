import time            
import re            
import os    
import sys  
import codecs  
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


def LoginWeibo(username, password):

    """
    This function takes the Weibo username and password and login to the Weibo homepage
    """
    try:
        #输入用户名/密码登录
        print(u'准备登陆Weibo.cn网站...')
        driver.get("https://login.sina.com.cn/signup/signin.php")
        elem_user = driver.find_element_by_name("username")
        elem_user.send_keys(username) #用户名
        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.send_keys(password)  #密码
        #uncheck auto login
        elem_auto = driver.find_element_by_xpath('//*[@id="remLoginName"]')
        elem_auto.click()
        
        time.sleep(3)
        
        elem_sub = driver.find_element_by_xpath("//input[@class='W_btn_a btn_34px']")
        elem_sub.click()              #点击登陆 因无name属性
        time.sleep(2)
                    
        print(u'登陆成功...')
        
        
    except Exception as e:      
        print("Error: ",e)
    finally:    
        print(u'End LoginWeibo!\n\n')
 
###search the weibo id of all artists
#verified account: //*[@id="pl_weibo_directtop"]/div/div/div/div[2]/p[1]/a[2]


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
    This function takes the name of the celebrity and password and search for weibo url of the celeb
    """
    
    name_search = driver.find_element_by_xpath('//*[@id="search_input"]')
    name_search.send_keys(name)
    submit_search = driver.find_element_by_xpath('//*[@id="search_submit"]')
    submit_search.send_keys(Keys.RETURN)
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after) #switch to the new tab
    #check if the verified account exists:
    time.sleep(5)
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
    driver = webdriver.Chrome('/Users/onyi/Dropbox/weibo/chromedriver')
    driver.set_page_load_timeout(45)
    wait = ui.WebDriverWait(driver,5)
    successful = False
    while not successful:
        LoginWeibo(username, password)
        if isElementPresent('//*[@id="search_input"]') == True:
            try:
                url=GetWeiboUrl(name)
                successful = True
            except TimeoutException:
                successful = False
                driver.refresh()
            except NoSuchElementException:
                successful =False
                driver.refresh()
        else:
            time.sleep(5)
            successful = False
            driver.refresh()
    
    print(name, url)
    urlfile = codecs.open("WeiboUrl.txt", 'a', 'utf-8')
    urlfile.write('=====================================================================\r\n')
    urlfile.write(u'Name: ' + name  + '\r\n')
    urlfile.write(u'url: ' + url  + '\r\n')
    urlfile.close()