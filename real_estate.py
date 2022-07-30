# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:04:29 2022

@author: Henrique
"""
#pip install pandas 
import re
#import time
#import urllib
#import requests

import pandas as pd

from bs4                            import BeautifulSoup
#from selenium                       import webdriver
#from bs4.element                    import CData
#from datetime                       import datetime
from urllib.request                 import urlopen



def get_links (url_realtor, pag):
    # number of pages of search result are 200, so we need to 
    page_numbers = list(range(pag))[1:pag]
    # list to store all the urls of properties
    list_of_links = []
    # for loop for all 200 search pages
    for page in page_numbers:
        # extracting html document of search page
        html1 = (home_url + '/p' + str(page) + '/?searchtypes=house+apartment')
        html = urlopen(html1)
        #print(html1)
        # parsing html document to 'lxml' format
        bsobj = BeautifulSoup(html, 'lxml')
        # finding all the links available in 'ul' tag whos 'data-testid' is 'results'
        all_links = bsobj.find('ul', 'tier-one-listing-table').findAll('a', href=re.compile('/international/br/*'))
        
        for link1 in all_links:
            # checking if it is a project and then performing similar thing I did above
            if 'href' in link1.attrs['href']:
                inner1_html = urlopen(link1.attrs['href'])
                inner1_bsobj = BeautifulSoup(inner1_html, "lxml")
                for link2 in inner1_bsobj.find('li', 'listing  ').findAll('a', href=re.compile('/international/br/*')):
                    if 'href' in link2.attrs:
                        list_of_links.append(link2.attrs['href'])
            else:
                list_of_links.append(link1.attrs['href'])
    
    # removing duplicate links while maintaining the order of urls
    links = []
    i_past = '10'
    for i in list_of_links: 
        if i not in links and re.findall(r'\d',str(i_past[:-2])) != re.findall(r'\d',str(i[:-2])):
            links.append(i)
            
            print(re.findall(r'\d',str(i_past[:-2])))
            print(re.findall(r'\d',str(i[:-2])))
            i_past = i
            
    return links




def create_df (links, url_h):
    # creating lists     
    all_basic_feature = []
    property_type_l = []
    price_l = []
    property_address_l = []
    lat_long_l = []
    not_open = []
    
    
    # loop to iterate through each url
    for link in links:
        print(link)
        # opening urls
        html1 = (home_url + link)
        while True:
            try:
                html = urlopen(html1)
                break
            except ValueError:
                not_open.append(html1)
                break
        #print(html1)
        
        # converting html document to 'lxml' format
        bsobj = BeautifulSoup(html, "lxml")
        
        # extracting address/name of property
        if bsobj.find_all('li', "address"):
            property_address_list = bsobj.find_all('li', "address")
            for property_address in property_address_list:
                property_address = property_address.find('span').text
            property_address_l.append(property_address)
        else:
            property_address_l.append('NA - property adress')
            
        #if bsobj.find_all('div', 'listing-map'):
        loc_list = bsobj.find_all('div', 'listing-map')
        for loc in loc_list:
            loc = loc.find('noscript')
            loc = re.findall(r'\D\d{2}.\d{6}',str(loc))
            if not loc:
                lat_long_l.append('NA - latitude/longitude')
            else:
                lat_long_l.append(loc[:2])
                            
        # extracting baths, rooms, parking etc
        if bsobj.find_all(title="Bedrooms"):
            bedroom_list = bsobj.find_all(title="Bedrooms")
            for bedroom in bedroom_list:
                bedrooms = bedroom.find('strong').text
            all_basic_feature.append(bedrooms)
        else:
            all_basic_feature.append('NA - bedroom')
    
        if bsobj.find_all(title="Bathrooms"):
            bathroom_list = bsobj.find_all(title="Bathrooms")
            for bathroom in bathroom_list:
                bathrooms = bathroom.find('strong').text
            all_basic_feature.append(bathrooms)
        else:
            all_basic_feature.append('NA - bathroom')
    
        if bsobj.find_all(title="House Size"):
            house_size_list = bsobj.find_all(title="House Size")
            for house_size in house_size_list:
                house_size = house_size.find('strong').text
            all_basic_feature.append(house_size)
        else:
            all_basic_feature.append('NA - house size')
            
        # extracting property price
        if bsobj.find_all("p", 'listing-price specified'):
            price_list = bsobj.find_all("p", 'listing-price specified')
            for price in price_list:
                price = price.find('strong').text.replace("""\n            \n     
                                                          BRL R$""",'').replace("""
                                                          \n            \n            """,'').replace("""            
                    From BRL R$""",'').replace(""" 
                
                """,'').replace("""
                
                    BRL R$ 
                
                """,'').replace("""
                
                    BRL R$""",'')
            price_l.append(price)
        else:
            price_l.append('NA - price')
        
         # extracting property type (house, ap...)
        if bsobj.find_all('li','property-type'):
            property_type_list = bsobj.find_all('li','property-type')
            for property_type in property_type_list:
                property_type = property_type.find('span').text
            property_type_l.append(property_type)
        else:
            property_type_l.append('NA - property type')
    
    
    
    x = all_basic_feature
    mat = []
    while x != []:
        mat.append(x[:3])
        x = x[3:]
    df_espec = pd.DataFrame(mat, columns=['quarto','banheiro','m²'])
    
    x = lat_long_l
    mat = []
    while x != []:
        mat.append(x[:1])
        x = x[1:]
    df_lat_long = pd.DataFrame(mat, columns=['lat & long'])
    
    x = property_address_l
    mat = []
    while x != []:
        mat.append(x[:1])
        x = x[1:]
    df_address = pd.DataFrame(mat, columns=['address'])
    
    x = price_l
    mat = []
    while x != []:
        mat.append(x[:1])
        x = x[1:]
    df_price = pd.DataFrame(mat, columns=['price'])
    
    x = property_type_l
    mat = []
    while x != []:
        mat.append(x[:1])
        x = x[1:]
    df_type = pd.DataFrame(mat, columns=['property type'])
    
    df = pd.concat([df_type,df_espec,df_address,df_lat_long,df_price], axis=1)
    
    #excel = df.to_excel("df.xlsx")
    #read_file = pd.read_excel ("df.xlsx")
    df.to_csv("df_houses.csv", index=None, header=True)
    df = pd.DataFrame(pd.read_csv("df_houses.csv"))
    
    return None


pages = 2
# home url
home_url = 'https://www.realtor.com/international/br/'
url = 'https://www.realtor.com'
links = get_links(home_url, pages)
create_df(links, url)