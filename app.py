from flask import Flask
import tempfile

from flask_restful import Api, Resource 

from bs4 import BeautifulSoup
from flask import request, jsonify
from tablib import Dataset
import os
import time
import urllib.parse
from werkzeug.utils import secure_filename
import pandas
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time

import json

app = Flask (__name__)

api= Api(app)



@app.route('/upload', methods=['POST'])
def upload() :

    data = request.json
    name = request.args.get('name')
    driver = webdriver.Chrome("C:\\Users\\smala\\Nouveau dossier\\chromedriver.exe")
    driver.get("https://linkedin.com/uas/login")
    

    for cookie in data:
        try:
            if 'sameSite' in cookie:
                if cookie['sameSite'] == 'no_restriction' or cookie['sameSite'] == 'unspecified' :
                    cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)
            pass
        except:
            cookie['domain'] == '.fr.linkedin.com'
            continue
        

    driver.get("https://linkedin.com/")
    print(type(name))
    x=name.split(',')
    print(x)
    NameList=[]
    my_dictionary = {}
    for j in x:
        if j.startswith('https'):
            driver.get(j)
        else:
            driver.get("https://"+j)    
        src = driver.page_source
        soup = BeautifulSoup(src,'lxml')
        delay = 8  
        mynewbuttonlist=[]
        

        try:
            time.sleep(2)
            button_span = WebDriverWait(driver, timeout=6).until(lambda d: driver.find_elements_by_xpath("//span[contains(@class, 'artdeco-button__text')]"))
            print(len(button_span))
            print(type(button_span[0].text.strip()))
            for i in range(0,len(button_span)):
                if button_span[i].text.strip() !='':
                    mynewbuttonlist.append(button_span[i].text.strip())

            print(mynewbuttonlist)
            if mynewbuttonlist[0]=="Se connecter":
                time.sleep(5)
                try:
                    buttone=driver.find_elements_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']")[1]
                    buttone.click()
                    buttone2=driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']")
                    buttone2.click()
                except IndexError:
                    buttone=driver.find_elements_by_xpath('//li-icon[@class="artdeco-button__icon"]')[3]
                    buttone.click()
                    buttone2=driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']")
                    buttone2.click()


                print("En attente")
                my_dictionary[j]="En attente"
            elif mynewbuttonlist[0]=="Suivre":
                time.sleep(5)
                buttone=driver.find_elements_by_xpath('//button[@aria-label="Plus d’actions"]')[1]
                buttone.click()
                sec=driver.find_elements_by_xpath('//li-icon[@class="mr3 flex-grow-0"]')[6]
                sec.click()
                try:

                    buttone2=driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']")
                    buttone2.click()
                except NoSuchElementException:
                    buttone2=driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view mr2']")
                    buttone2.click()
                    buttone3=driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']")
                    buttone3.click()


                print("En Attente")
                my_dictionary[j]="En atttente"
            elif mynewbuttonlist[0]=="Suivi" or mynewbuttonlist[0]=="Rédiger un message":    
                print("CONNECTION")
                my_dictionary[j]="Connected"
            elif mynewbuttonlist[0]=="Message" :    
                print("En attente")
                my_dictionary[j]="En attente"    
            elif mynewbuttonlist[0]=="En attente": 
                print("En attente")
                my_dictionary[j]="En attente" 

            time.sleep(3)    




            '''
            
            if(button_span[0].text.strip()=="Se connecter"):
                buttone=driver.find_elements_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']")[1]
                buttone.click()
                my_dictionary[j]="Se connecter"
            if(button_span[0].text.strip()=="Suivre"): 
                buttone=driver.find_elements_by_xpath('//button[@aria-label="Plus d’actions"]')[1]
                buttone.click()
                time.sleep(5)
                sec=driver.find_elements_by_xpath('//li-icon[@class="mr3 flex-grow-0"]')[6]
                sec.click()
                time.sleep(5)
                my_dictionary[j]="Suivre"

            '''    
                    
                
        except (TimeoutException):
            print ("trying again")
                


        


            
            
            
        

 
        
        '''
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button')))
            print ("Page is ready!")
            try:
                invitation_div = soup.find('div', {'class' : 'pv-top-card-v2-ctas display-flex pt2' })
                sous_invitation_div=invitation_div.find('div', {'class' : 'pvs-profile-actions' })
                button_span=sous_invitation_div.find('span', {'class' : 'artdeco-button__text' })
                button2=sous_invitation_div.find('button', {'class' : 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action' })
                print(button_span.text.strip())
                print(len(button_span.text.strip()))
                myElem.submit()
                
            except :
                print("Error")
        except TimeoutException:
            print ("Loading took too much time!")
        '''


    """

        try:
            invitation_div = soup.find('div', {'class' : 'pv-top-card-v2-ctas display-flex pt2' })
            sous_invitation_div=invitation_div.find('div', {'class' : 'pvs-profile-actions' })
            button_span=sous_invitation_div.find('span', {'class' : 'artdeco-button__text' })
            button2=sous_invitation_div.find('button', {'class' : 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action' })
            print(button_span.text)
        except :
            print("Error")


        """



        
        
        
        

        
       
        
        
    
    
    #src = driver.page_source
    #soup = BeautifulSoup(src,'lxml')

    #name_div = soup.find('div', {'class' : 'mt2 relative' })

    #name_clear = name_div.find('h1', {'class' : 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
    s = ','.join(NameList)

    return my_dictionary






if __name__ == "__main__" : 
    app.run(debug=True,threaded=True)