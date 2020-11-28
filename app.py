import requests
from selenium import webdriver
from utils import keys
import time
from datetime import datetime
from threading import Timer
import re


def execute_sec(driver,xpath,type,key):              #wait the xpath element appear then execute task (less latency)
    el = driver.find_elements_by_xpath(xpath);
    while (not el):
        el=driver.find_elements_by_xpath(xpath)
        time.sleep(1)
    if(type=='input'):
            el[0].send_keys(keys[key])
    if(type=='click'):
            el[0].click()
    return 


def login(driver):
    driver.get('https://agende.unipi.it/bno-irb-rbh')
    execute_sec(driver,'/html/body/div/form[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]','input','email')
    execute_sec(driver,'/html/body/div/form[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/div/div/input','click','null')
    
    #Logging UNIPI page
    execute_sec(driver,'/html/body/div[2]/div[2]/div/div[1]/form/div[1]/input','input','user')
    execute_sec(driver,'/html/body/div[2]/div[2]/div/div[1]/form/div[2]/input','input','password')
    execute_sec(driver,'/html/body/div[2]/div[2]/div/div[1]/form/div[5]/button','click','null')

    #Keep logged
    execute_sec(driver,'/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input','click','null')
    return

def book(driver,day,column):
    #find the column of current day
    curr=0
    time.sleep(2)
    offset=2
    for x in range(7):
        s = driver.find_element_by_xpath("/html/body/div/section/div/div/div/div/div[2]/div/table/thead/tr/td/div/table/thead/tr/th[{}]/a".format(offset+x)).text
        if(s[4:-3]==day):
            curr=x+offset;

    #book
    time.sleep(3)
    execute_sec(driver,"/html/body/div/section/div/div/div/div//div[2]/div/table/tbody/tr/td/div[2]/div/div[3]/table/tbody/tr/td[{}]/div/div[2]/a[{}]/div/div[2]".format(curr,column),"click","null")

if __name__ == '__main__':

    x=datetime.today()

    if(keys["dayeven"]=="1"):
        start = x.replace(day=int(keys["day"]), hour=int(keys["day_h"]), minute=int(keys["day_m"]), second=0, microsecond=0)
        delta_t = start-x

    if(keys["dayeven"]=="2"):
        start=x.replace(day=int(keys["day"]), hour=int(keys["eve_h"]), minute=int(keys["eve_m"]), second=0, microsecond=0)
        delta_t = start-x

    if(x<start):
        time.sleep(delta_t.seconds) #Waiting until you can book
        driver = webdriver.Chrome('./chromedriver')
        login(driver)
        print("LOGGED")
        book(driver,keys['day'],keys["dayeven"])
        print("BOOKED")
        time.sleep(7)
        driver.quit()
    else:
        print("Il tempo per prenotarsi è scaduto")



    



