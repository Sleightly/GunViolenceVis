import requests
import urllib
import pandas as pd
import numpy as np

df = pd.read_csv('GunViolenceVis/gv_data.csv')
df = df[np.isfinite(df['latitude']) & np.isfinite(df['longitude'])]
df['n_casualties'] =  df.apply(lambda row: row.n_killed + row.n_injured, axis=1)

df_fips = df[df['n_casualties'] >= 3]

county_fips = []

for lat, lon, n in zip(df_fips['latitude'], df_fips['longitude'], df_fips['n_casualties']):
    if n >= 3:
        #Encode parameters 
        params = urllib.parse.urlencode({'latitude': lat, 'longitude': lon, 'format':'json'})
        #Contruct request URL
        url = 'https://geo.fcc.gov/api/census/block/find?' + params

        #Get response from API
        response = requests.get(url)

        #Parse json in response
        data = response.json()

        #Print FIPS code
        try:
            print(data['County']['FIPS'])
            county_fips.append(data['County']['FIPS'])
        except:
            county_fips.append(np.nan)
print(county_fips)