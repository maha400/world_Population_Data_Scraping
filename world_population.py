# -*- coding: utf-8 -*-
"""world_population.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18ZpLpocM0BOkovhwAMHimPLX8QezO7Oa
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook

url='https://www.worldometers.info/world-population/population-by-country/'
html_data=requests.get(url).text
soup=BeautifulSoup(html_data,'html.parser')
#print(soup)

#build the data frame

population_df=pd.DataFrame(columns=['country','population','yearly change','net change','density','land area(km2)'
                                    ,'migrants','fert rate','urban pop'])
table=soup.find('table', id='example2')
#print(table)

#filling th data frame

for row in table.find_all('tr'):
    col =row.find_all('td')
    if len(col)!=0:
        data_to_append = pd.DataFrame({
        'country': [col[1].text],
        'population': [col[2].text],
        'yearly change': [col[3].text],
        'net change': [col[4].text],
        'density': [col[5].text],
        'land area(km2)': [col[6].text],
        'migrants': [col[7].text],
        'fert rate': [col[8].text],
        'urban pop': [col[10].text]
        })
        #print(data_to_append)
# Concatenate the new DataFrame with the original DataFrame
        population_df = pd.concat([population_df, data_to_append], ignore_index=True)
population_df

####### columns types
population_df[['population','land area(km2)','density','migrants','net change']] = population_df[['population','land area(km2)','density','migrants','net change']].replace(',', '', regex=True).astype(int)
population_df[['yearly change','urban pop']]=population_df[['yearly change','urban pop']].replace('%','',  regex=True)
population_df['yearly change']=population_df['yearly change'].astype(float)
#population_df['urban pop']=population_df['urban pop'].replace("N.A.", float("NaN"), inplace=True)
population_df['urban pop'] = pd.to_numeric(population_df['urban pop'], errors='coerce')
population_df['fert rate'].replace("", "N.A.", inplace=True)
population_df['fert rate'] = pd.to_numeric(population_df['fert rate'], errors='coerce')
population_df.dtypes
population_df

##  data cleaning
fert_mean=population_df['fert rate'].mean()
urban_pop_mean=population_df['urban pop'].mean()

population_df['fert rate'].fillna(fert_mean , inplace=True)
population_df['urban pop'].fillna(urban_pop_mean , inplace=True)

population_df.isna().sum()
population_df

population_df.dtypes

## columns rename
population_df.rename(columns={'urban pop': 'urban pop(%)','fert rate':'fert rate (%)' },  inplace=True)
population_df

population_df.to_csv('world_population.csv',index=False)
population_df.to_excel('world_population.xlsx',index=False)