import base64
import functions_framework

import re
import os
import gcsfs
import fsspec
import pyodbc
import urllib

import pandas as pd

#from google.cloud                   import storage
#from oauth2client.service_account   import ServiceAccountCredentials
from bs4                            import BeautifulSoup
#from pathlib                        import Path
from datetime                       import datetime
from sqlalchemy                     import create_engine
from urllib.request                 import urlopen



def get_links (url_realtor_br, pag):
    # number of pages of search result 
    page_numbers = list(range(pag+1))[1:pag+1]
    # list to store all the urls of properties
    list_of_links = []
    # for loop for all search pages
    for page in page_numbers:
        # extracting html document of search page
        while True:
            try:
                html1 = (url_realtor_br + '/p' + str(page) + '/?searchtypes=house+apartment')
                html = urlopen(html1)
                #print(html1)
                break
            except ValueError:
                break
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
    i_past = '00'
    for i in list_of_links: 
        if i not in links and re.findall(r'\d',str(i_past[:-2])) != re.findall(r'\d',str(i[:-2])):
            links.append(i)
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
        #print(link)
        # opening urls
        html1 = (url_h + link)
        while True:
            try:
                html = urlopen(html1)
                break
            except ValueError:
                not_open.append(html1)
                break
        
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
            
        # extracting location lat and long
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
            all_basic_feature.append('0')
    
        if bsobj.find_all(title="Bathrooms"):
            bathroom_list = bsobj.find_all(title="Bathrooms")
            for bathroom in bathroom_list:
                bathrooms = bathroom.find('strong').text
            all_basic_feature.append(bathrooms)
        else:
            all_basic_feature.append('0')
    
        if bsobj.find_all(title="House Size"):
            house_size_list = bsobj.find_all(title="House Size")
            for house_size in house_size_list:
                house_size = house_size.find('strong').text
            all_basic_feature.append(house_size)
        else:
            all_basic_feature.append('0')
            
        # extracting property price
        if bsobj.find_all("p", 'listing-price specified'):
            price_list = bsobj.find_all("p", 'listing-price specified')
            for price in price_list:
                price = price.find('strong').text.replace("""\n            \n     
                                                          BRL R$""",'').replace("""
                                                          \n            \n            """,'').replace("""            
                    From BRL R$""",'').replace("""
                
                    BRL R$""",'').replace("""
                
                    BRL R$""",'').replace("""
            
                From BRL R$""","").replace(' ','').replace("""
            
                BRL R$""","").replace("""
BRLR$""",'').replace('  ','')
            price_l.append(price)
        else:
            price_l.append('0')
        
         # extracting property type (house, ap...)
        if bsobj.find_all('li','property-type'):
            property_type_list = bsobj.find_all('li','property-type')
            for property_type in property_type_list:
                property_type = property_type.find('span').text.replace(' ','')
            property_type_l.append(property_type)
        else:
            property_type_l.append('NA - property type')
    
    # creating dfs
    x = all_basic_feature
    mat = []
    while x != []:
        mat.append(x[:3])
        x = x[3:]
    df_espec = pd.DataFrame(mat, columns=['bedroom','bathroom','m²'])
    
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
    
    # concat all dfs
    df = pd.concat([df_type,df_espec,df_address,df_lat_long,df_price], axis=1)

    # create csv file with timestamp
    now = datetime.now() # current date and time (%m.%d.%Y,%H.%M.%S)
    date_time = now.strftime("%m.%d.%Y")
    name_df = 'df_houses p1 - ' + str(date_time) + '.csv'
    #filepath = Path('gs://archive_real_estate/csv/' + name_df)
    filepath = 'gs://archive_real_estate/csv/' + name_df
    #print(filepath)
    #filepath.parent.mkdir(parents = True, exist_ok = True)
    
    df.to_csv(filepath, index = None, header = True)
    
    #client = storage.Client()
    # Replace the string below with a unique name for the new bucket
    #bucket_name = 'archive_real_estate'
    #bucket = client.get_bucket(bucket_name)

    # Creates the new bucket
    #bucket = client.create_bucket(bucket_name)
    
    #blob_name = name_df
    #blob = bucket.blob(name_df)

    #source_file_name = name_df
    #file = df.to_csv(index=None, header=True)
    #blob.upload_from_filename(file)

    #bucket = client.get_bucket('gs://archive_real_estate/csv/')
    #blob = bucket.blob(name_df)
    #blob.upload_from_filename(name_df)
    print('OK')

    
    
    #df.to_csv(filepath, index=None, header=True)
    #df = pd.DataFrame(pd.read_csv(filepath))
    
    # csv file for site not open
    if len(not_open) != 0:
        df_nt_open = pd.DataFrame(not_open, columns=['sites not open'])
        df_nt_open.to_csv("gs://archive_real_estate/csv/df_sites_not _open_p1.csv", index = None, header = True)
    
    return df



#def save_db (df):
#    while True:
#        try:
#            # connect the DB
#            server = "HENRIQUE\SQLEXPRESS01"
#            db = "Real Estate db"
#            quoted = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+db+';Trusted_Connection=yes')
#            engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
            
#            command = """DROP TABLE IF EXISTS real_estate_db"""
#            engine.execute(command)
 
#            df.to_sql('real_estate_db', con=engine, if_exists='append')
#            status = 'OK'
#            break
#        except ValueError:
#            status = 'Error to connect with DB'
#            break
    
#    return status

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.http
def hello_http(request):
   # Print out the data from Pub/Sub, to prove that it worked
   #print(base64.b64decode(cloud_event.data["message"]["data"]))

    # timestamp start
    now = datetime.now() # current date and time (%m.%d.%Y,%H.%M.%S)
    start = now.strftime("%m.%d.%Y, %H:%M:%S")
    print("Start: ", start)
    
    # call def
    pages = 100  #input("Enter a number of pages: ")
    url = 'https://www.realtor.com/international/br/'
    home_url = 'https://www.realtor.com'
    links = get_links(url, int(pages))
    create_df(links, home_url)
    #status = save_db(df)
    #print(status)
    
    # timestamp end
    now = datetime.now() # current date and time (%m.%d.%Y,%H.%M.%S)
    end = now.strftime("%m.%d.%Y, %H:%M:%S")
    print("End: ", end)
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
       name = request_json['name']
    elif request_args and 'name' in request_args:
       name = request_args['name']
    else:
       name = 'World'
    return 'Hello {}!'.format(name)