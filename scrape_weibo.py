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
from datetime import datetime


class Weibo(object):
    
    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password
    
        
    def LoginWeibo(self):
        
        success = False
        while success == False:
            
            try:
            #输入用户名/密码登录
                print(u'准备登陆Weibo.cn网站...')
            
                self.driver.get("https://login.sina.com.cn/signup/signin.php")
                WebDriverWait(self.driver, 8).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                elem_user = self.driver.find_element_by_name("username")
                elem_user.send_keys(self.username) #用户名
                elem_pwd = self.driver.find_element_by_name("password")
                elem_pwd.send_keys(self.password)  #密码
                #uncheck auto login
                elem_auto = self.driver.find_element_by_xpath('//*[@id="remLoginName"]')
                elem_auto.click()
                time.sleep(3)
                elem_sub = self.driver.find_element_by_xpath("//*[@id='vForm']/div[2]/div/ul/li[7]/div[1]/input")
                elem_sub.click()              #点击登陆 因无name属性
                #check if successfully login:
                time.sleep(5)
                WebDriverWait(self.driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                                
                #check if front page is loaded
                if self.isElementPresent('//*[@id="SI_TopBar"]/div/p/a') == True:
                    success = True
                else:
                    pass                  
            
            except Exception as e:      
                print("Error: ",e)
            finally:    
                print(u'登陆成功...!\n\n')
        
        
    def SaveActivePage(self, userid):
        """
        This function sabes all the weibo tweets including the text, time, number of comments
        , number of post and number of support in the current page.  
        """
        output = codecs.open('weibo/%s.txt' %userid , 'a', 'utf-8')
        
        if self.isElementPresent("//*[@id='Pl_Official_MyProfileFeed__20']/div/div[2]/div[1]/div[4]/div[3]")==False:
            for i in range (10, 50):
                elem = "//*[@id='Pl_Official_MyProfileFeed__%d']" %i
                if self.isElementPresent(elem) == False:
                    continue
                else:
                    break
            print(elem)
            
           
        for i in range(2, 60):
            try:
                text_elem = elem + "/div/div[%d]/div[1]/div[3]/div[3]" % i
                time_elem = elem + "/div/div[%d]/div[1]/div[3]/div[2]/a[1]" % i
                repost_elem = elem + "/div/div[%d]/div[2]/div/ul/li[2]/a/span/span/span/em[2]" % i
                comment_elem = elem + "/div/div[%d]/div[2]/div/ul/li[3]/a/span/span/span/em[2]" % i
                support_elem = elem + "/div/div[%d]/div[2]/div/ul/li[4]/a/span/span/span/em[2]" % i
                oripost_author = elem + "/div/div[%d]/div[1]/div[3]/div[4]/div[2]/div[1]/a[1]" %i
                origpost_elem =  "/div/div[%d]/div[1]/div[3]/div[4]/div[2]/div[2]" % i
                
                
                if self.isElementPresent(text_elem) == False:
                    text_elem = elem + "/div/div[%d]/div[1]/div[4]/div[3]" % i
                    time_elem = elem + "/div/div[%d]/div[1]/div[4]/div[2]/a[1]" % i
                else:
                    pass
                
           
                weibo_text = self.driver.find_element_by_xpath(text_elem).text       
                Time = self.driver.find_element_by_xpath(time_elem).text
                Comment_count = self.driver.find_element_by_xpath(comment_elem).text
                Repost_count = self.driver.find_element_by_xpath(repost_elem).text
                Support_count = self.driver.find_element_by_xpath(support_elem).text
                
                
                output.write(u'text: ' + weibo_text + '\r\n')
                output.write(u'date: ' + str(Time) + '\r\n')
                output.write(u'repost: ' + str(Repost_count) + '\r\n')
                output.write(u'comment: ' + str(Comment_count) + '\r\n')
                output.write(u'support: ' + str(Support_count) + '\r\n')
                if self.isElementPresent(oripost_author) == True:
                    Origpost_author = self.driver.find_element_by_xpath(oripost_author).text
                    Origpost_text = self.driver.find_element_by_xpath(origpost_elem).text
                    output.write(u'Original Author: ' + str(Origpost_author) + '\r\n')
                    output.write(u'Original Post: ' + str(Origpost_text) + '\r\n')
                else:
                    pass
                output.write('=====================================================================\r\n')
        
            except NoSuchElementException: #if the text element cannot be located, try to find if it's a shared post
               
                try:
                    share_elem = elem + "/div/div[%d]/div[2]/div[3]/div[3]" %i
                    share_author = elem + "/div/div[%d]/div[2]/div[3]/div[1]/a" %i
                    Share_author = self.driver.find_element_by_xpath(share_author).text
                    Share_text = self.driver.find_element_by_xpath(share_elem).text
                    output.write(u'Share Author: ' + str(Share_author) + '\r\n')
                    output.write(u'Share Post: ' + str(Share_text) + '\r\n')
                    output.write('=====================================================================\r\n')
                    
                except NoSuchElementException: 
                    
                    try: 
                        commentshare_elem = elem + "/div/div[%d]/div[1]/div[3]/div[3]" %i
                        oripost_elem = elem + "/div/div[%d]/div[1]/div[3]/div[4]/div[2]/div[2]" %i
                        oriauthor_elem = elem + "/div/div[%d]/div[1]/div[3]/div[4]/div[2]/div[1]/a[1]" %i
                        owncomment = self.driver.find_element_by_xpath(commentshare_elem).text
                        ori_author = self.driver.find_element_by_xpath(oriauthor_elem).text
                        ori_text = self.driver.find_element_by_xpath(oripost_elem).text
                        output.write(u'Own Comment: ' + str(owncomment) + '\r\n')
                        output.write(u'Original Author: ' + str(ori_author) + '\r\n')
                        output.write(u'Original Post: ' + str(ori_text) + '\r\n')
                        output.write('=====================================================================\r\n')
                        
                    except NoSuchElementException:
                        
                        try:   
                            fwdtext_elem = elem + "/div/div[%d]/div[2]/div[4]/div[3]" %i
                            fwdauthor_elem = elem + "/div/div[%d]/div[2]/div[4]/div[1]/a[1]" %i
                            oriauthor_elem = elem + "/div/div[%d]/div[2]/div[4]/div[4]/div[2]/div[1]/a[1]" %i
                            oripost_elem = elem + "/div/div[%d]/div[2]/div[4]/div[4]/div[2]/div[2]" %i
                
                            fwdcomment = self.driver.find_element_by_xpath(fwdtext_elem).text
                            fwd_author = self.driver.find_element_by_xpath(fwdauthor_elem).text
                            ori_author = self.driver.find_element_by_xpath(oriauthor_elem).text
                            ori_text = self.driver.find_element_by_xpath(oripost_elem).text
                            
                            output.write(u'Forward Comment (By another ID): ' + str(fwdcomment) + '\r\n')
                            output.write(u'Forward Author (By another ID): ' + str(fwd_author) + '\r\n')
                            output.write(u'Original Author: ' + str(ori_author) + '\r\n')
                            output.write(u'Original Post: ' + str(ori_text) + '\r\n')
                            output.write('=====================================================================\r\n')
                            
                        except NoSuchElementException: 
                            output.write('Element cannot be located\r\n')
                            output.write('=====================================================================\r\n')
                            print("can't find the element:", share_elem)
                            time.sleep(1)
    
        output.close()
        
        if len(Time) > 12:
            Time = Time.replace('-1-','-01-')
            Time.replace('-2-','-02-')
            Time.replace('-3-','-03-')
            Time.replace('-4-','-04-')
            Time.replace('-5-','-05-')
            Time.replace('-6-','-06-')
            Time.replace('-7-','-07-')
            Time.replace('-8-','-08-')
            Time.replace('-9-','-09-')
            date = datetime.strptime(Time, '%Y-%m-%d %H:%M')
        
        return(date.year)


    def isElementPresent(self,locator):
        try:
            self.driver.find_element_by_xpath(locator)
        except NoSuchElementException:
            return False
        return True


    def GetMaxPage(self, url):
        """
        This function returns the maximum number of weibo pages that a user has.
        """
        print('maxpage', url)
        try:
            self.driver.set_page_load_timeout(30)
            self.driver.get(url)
        except TimeoutException:
            try:
                self.driver.refresh()
                self.driver.get(url)
            except TimeoutException:
                print('cannot load page')
            
        successful = False
    
        while successful == False:
            try:
                for i in range(1,5):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(3)
                WebDriverWait(self.driver, 8).until(lambda d: d.execute_script('return document.readyState') == 'complete')
         
                if self.isElementPresent("//div[@class='W_pages']/span/a[@action-data]") == False:
                    print('XXXXXX')
                    self.driver.refresh()
                    time.sleep(10)
                    successful = False
                else:
                    page_elem = self.driver.find_element_by_xpath("//div[@class='W_pages']/span/a[@action-data]")   
                    maxpage = int(page_elem.get_attribute("action-data").split("countPage=",1)[1])
                    print('maxpage:', maxpage)
                    successful = True
            except NoSuchElementException:
                successful = False
            except TimeoutException:
                print("Loading took too much time!")
                self.driver.refresh()
                successful = False
        
        return(maxpage)


    def VisitPersonPage(self, userid):
            
        userfile = codecs.open("weibo/user_stats.txt", 'a', 'utf-8') 
        
        try:
            
            str_name = self.driver.find_element_by_xpath("//div[@class='pf_username']/h1")
            name = str_name.text        #str_name.text是unicode编码类型
            print(u'昵称: ', name)
        
            #关注数 粉丝数 微博数 <td class='S_line1'>
            str_elem = self.driver.find_elements_by_xpath("//table[@class='tb_counter']/tbody/tr/td/a")
            str_gz = str_elem[0].text    #关注数
            num_gz = re.findall(r'(\w*[0-9]+)\w*', str_gz)
            str_fs = str_elem[1].text    #粉丝数
            num_fs = re.findall(r'(\w*[0-9]+)\w*', str_fs)
            str_wb = str_elem[2].text    #微博数
            num_wb = re.findall(r'(\w*[0-9]+)\w*', str_wb)
     
            #文件操作写入信息
            userfile.write('=====================================================================\r\n')
            userfile.write(u'用户: ' + userid + '\r\n')
            userfile.write(u'昵称: ' + name + '\r\n')
            userfile.write(u'关注数: ' + str(num_gz[0]) + '\r\n')
            userfile.write(u'粉丝数: ' + str(num_fs[0]) + '\r\n')
            userfile.write(u'微博数: ' + str(num_wb[0]) + '\r\n')
        
        
        except Exception as e:      
            print("Error: ",e)
        finally:    
            print(u'Done!\n\n')
            
        userfile.close()
        
        
    def Scrape(self): 
        """
        This function scrolls down the active page to load all weibo tweets, save all content, and then move to the next page
        """
        url2 = self.url + "?profile_ftype=1&is_all=1#_0"
        print(url2)
        maxpage = self.GetMaxPage(url2)
        if 'u/' in self.url:
            userid = self.url.split(".com/u/",1)[1] 
        else:
            userid = self.url.split(".com/",1)[1] 
    
        output = codecs.open("weibo/%s.txt" %userid, 'w', 'utf-8') #create user id file
        output.close()
    
        for i in range(1,maxpage+1): #go to each weibo page
            #select all post, not just the default "hot" ones
            url1 = self.url + "?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=" + str(i) + "#feedtop"
            loadpage = False
            while loadpage == False:
                try:
                    print(url1)
                    self.driver.get(url1)
                    time.sleep(5)
                except TimeoutException:
                    self.driver.refresh()
                    loadpage = False
                finally:
                    loadpage = True
            
            #scroll to bottom to load page
            for j in range(1,5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)
                WebDriverWait(self.driver, 8).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
            print('page is scrape ready')
            if i == 1:
                self.VisitPersonPage(userid)
                
            YearLastWeibo = self.SaveActivePage(userid)
            
            if YearLastWeibo < 2016: #retrive only tweets in as far back as 2016
                break
       
        self.driver.close()
    
     