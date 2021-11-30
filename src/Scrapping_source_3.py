#!/usr/bin/env python
# coding: utf-8

#import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

#load webpage https://www.theguardian.com/football
# headers will be used to trick the website that we open it like a browser, not like a scrapping tool. 
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
page = 'https://www.theguardian.com/football/premierleague/table'
try:
    content = requests.get(page, headers=headers)
except:
    print('Source 1 unavailable. Check the internet connection')
soup = BeautifulSoup(content.content, 'html.parser')
#identify columns from content page
player_table = soup.find("table")
columns = []
for th in player_table.find_all('th'):
    title = th.text
    columns.append(title)
data_tg = pd.DataFrame(columns = columns)
leagues = ['premierleague', 'bundesligafootball', 'serieafootball', 'laligafootball', 'ligue1football']
for league in leagues:
    page = 'https://www.theguardian.com/football/'+ league + '/table'
    try:
        content = requests.get(page, headers=headers)
    except:
        print('Source 1 unavailable. Check the internet connection')
    soup = BeautifulSoup(content.content, 'html.parser')
    #identify columns from content page
    player_table = soup.find("table")
    listo = []
    for tr in player_table.find_all('tr'):
            data = tr.find_all('td')
            for tr in data:
                item = tr.text
                listo.append(item.strip())
    for i in range(0, len(listo), len(columns)):
        kalisto = listo[i:i + len(columns)]            
        data_tg_length = len(data_tg)
        data_tg.loc[data_tg_length] = kalisto

# make copy of data_frame
df_source3 = data_tg.copy()

# drop unnecessary columns and change type to numeric continuous variables
# create a new variable avg_points 
df_source3 = df_source3.drop(['P','Form'], axis=1)
df_source3[['GP', 'W', 'D', 'L','F', 'A', 'GD', 'Pts']] = df_source3[['GP', 'W', 'D', 'L','F', 'A', 'GD', 'Pts']].apply(pd.to_numeric) 
df_source3['club_avg_points']=df_source3['Pts'] / df_source3['GP']

# rename a column
df_source3.rename(columns={'Team': 'club'}, inplace = True)

# checking our DataFrame
df_source3

# export our data into csv file.
df_source3.to_csv('../data/df_source3.csv', index=False)
print("df_source3 is exported to '../data/df_source3.csv'")