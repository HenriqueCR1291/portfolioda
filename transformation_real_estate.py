import re
import functions_framework

import pandas     as pd
from datetime     import datetime


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.http
def hello_http(request):
    # upload the dfs
    now = datetime.now() # current date and time (%m.%d.%Y,%H.%M.%S)
    date_time = now.strftime("%m.%d.%Y")
    name_df_1 = 'df_houses p1 - ' + str(date_time) + '.csv'
    name_df_2 = 'df_houses p2 - ' + str(date_time) + '.csv'
    filepath_1 = 'gs://archive_real_estate/csv/' + name_df_1
    filepath_2 = 'gs://archive_real_estate/csv/' + name_df_2
    
    df1 = pd.read_csv(filepath_1)
    df2 = pd.read_csv(filepath_2)
    
    df = pd.concat([df1, df2])
    
    # delete white spaces
    df['price'] = df['price'].str.strip()
    df['property type'] = df['property type'].str.strip()
    df['property type'] = df['property type'].apply(lambda x: re.sub(r"^(.*)(\bNewResidentialDevelopment\b)(.*?)", 'New Residentia Development', x))
    df['m²'] = df['m²'].str.strip()
    
    
    # drop duplicates
    df = df.reset_index(drop=True)
    df['concat'] = pd.Series(df[['property type','bedroom', 'bathroom', 'm²', 'address', 'lat & long', 'price']].values.tolist()).str.join('/')
    df = df.drop_duplicates()
    del df['concat']
    
    
    # transform data
    df['address'] = df['address'].apply(lambda x: x.replace('ENDEREÇO NÃO INFORMADO, ',''))
    df['address'] = df['address'].apply(lambda x: x.replace(', Address available on request',''))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\bRua \b)(.*?), ", '', x))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\bRodovia \b)(.*?), ", '', x))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\bEstrada \b)(.*?), ", '', x))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\bRod. \b)(.*?), ", '', x))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\bAvenida \b)(.*?), ", '', x))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\bAv. \b)(.*?), ", '', x))
    df['address'] = df['address'].apply(lambda x: re.sub(r"^(.*)(\d)(.*?), ", '', x))
    
    df['price'] = df['price'].apply(lambda x: re.sub(r",",'.', x))
    df['price'] = df['price'].apply(lambda x: re.sub(r"$",',00', x))
    
    df['m²'] = df['m²'].apply(lambda x: re.sub(r",",'.', x))
    df['m²'] = df['m²'].apply(lambda x: re.sub(r".\d{2}$",'', x))
    
    # save final file
    name_df = 'df_houses - ' + str(date_time) + '.csv'
    filepath = 'gs://archive_real_estate/csv/final_df' + name_df
    df.to_csv(filepath, index = None, header = True)
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
       name = request_json['name']
    elif request_args and 'name' in request_args:
       name = request_args['name']
    else:
       name = 'World'
    return 'Hello {}!'.format(name)