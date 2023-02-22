import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import numpy as np
import pandas as pd

class Graber: 
    
    url = 'https://apteki.su/'
    city = ''

    def __init__(self, city = ''):
        if city != '':
            self.city = city
            self.url = f"https://{city}.apteki.su//catalog//Оземпик"

    def openDriver(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def waitLoadElement(self):    
        pass
    
    def getCity(self):
        places = None
        city_list = []
        try:
            element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@class='location-window__list location-window__list_city']")))
        finally:
            while places is None:
                places = self.driver.execute_script("return sessionStorage.getItem('places');")

            places_json = json.loads(places)
            
            for place in places_json:
                city_list.append(place['alias'])
            city_list.sort()
        return city_list

    def getPrice(self):
        table = self.driver.find_element(By.CLASS_NAME, 'search-select-form__item-list')
        elements = table.find_elements(By.TAG_NAME, 'dl')
        element_array = []
        for element in elements:
            name = element.find_elements(By.TAG_NAME, 'dt')[0].text
            price = element.find_elements(By.TAG_NAME, 'dd')[0].text
            element_array.append([self.city, name, price])
        return element_array
        
    def closeDriver(self):
        self.driver.quit()

#MAIN
#get all city`s
graber = Graber()
graber.openDriver()
city_list = graber.getCity()
graber.closeDriver()


#get price in some city
prices = []
for city in city_list:
    try:
        graber = Graber(city)
        graber.openDriver()
        pricesInCity = graber.getPrice()
        for priceInCity in pricesInCity:
            prices.append(priceInCity)
        print (f'{city} --- grabed')
    except:
        prices.append([city, 'nil', 'nil'])
        print (f'{city} --- error')
        
    graber.closeDriver()


#save to csv
df = pd.DataFrame(prices, columns = ['city', 'name', 'price'])
df.to_csv('test.csv', index=False)
