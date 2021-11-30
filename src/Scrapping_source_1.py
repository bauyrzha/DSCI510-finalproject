#!/usr/bin/env python
# coding: utf-8


#import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd


#load webpage https://www.transfermarkt.co.uk
# headers will be used to trick the website that we open it like a browser, not like a scrapping tool. 
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
page = 'https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&altersklasse=alle&ausrichtung=alle&jahrgang=0&kontinent_id=0&land_id=0&page=1&plus=1&spielerposition_id=alle'
try:
    content = requests.get(page, headers=headers)
except:
    print('Source 1 unavailable. Check the internet connection')
soup = BeautifulSoup(content.content, 'html.parser')
#identify columns from content page
player_table = soup.find("table", attrs={"class": "items"})
columns = []
for th in player_table.find_all('th'):
    title = th.text
    if title !='':
        columns.append(title)
    else:
        columns.append(th.find('div').get('title')) # in the website not all headers have values, it uses icons, therefore we get title value  
# below when we scrap the data we will get some unnecessary items
# we create some extra columns, then we will drop them 
columns.insert(1, "delete1")
columns.insert(2, "delete2")
columns.insert(4, "position")
columns2 = ["delete3","delete4", "delete5"]
columns.extend(columns2)
# create DataFrame with necessary columns 
data_tm = pd.DataFrame(columns = columns)

# Because of necessary data are divided into 20 webpages, we will use for loop  
for i in range(1,21):
    page = 'https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&altersklasse=alle&ausrichtung=alle&jahrgang=0&kontinent_id=0&land_id=0&page=' + str(i) + '&plus=1&spielerposition_id=alle'
    try:
        content = requests.get(page, headers=headers)
    except:
        print('Source 1 unavailable. Check the internet connection')
    soup = BeautifulSoup(content.content, 'html.parser')
    #scrap data from content page
    listo = []
    player_table = soup.find("table", attrs={"class": "items"})
    for tr in player_table.find_all('tr'):
        data = tr.find_all('td')
        for tr in data:
            item = tr.text
            if  item !='':
                listo.append(item)
            else:
                listo.append(tr.find('img').get('alt')) # where images are used instead of item, we get information from images.
    # insert data into DataFrame
    for i in range(0, len(listo), len(columns)):
        kalisto = listo[i:i + len(columns)]            
        data_tm_length = len(data_tm)
        data_tm.loc[data_tm_length] = kalisto

# make copy of data_frame
df_source1 = data_tm.copy()

# rename a column
df_source1.rename(columns={'Player': 'name'}, inplace = True)

# leave only necessary columns
df_source1 = df_source1[['name', 'position', 'Age', 'Nat.', 'Market value', 'club', 'Goals', 'Assists']] 

# checking our DataFrame
df_source1

# export our data into csv file.
df_source1.to_csv('../data/df_source1.csv', index=False)
print("df_source1 is exported to '../data/df_source1.csv'")




