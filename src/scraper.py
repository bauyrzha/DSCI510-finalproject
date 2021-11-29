# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 21:04:10 2021

@author: Yerke
"""

#import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import http.client
import json
import time

#my api_key. You will receive your own if you register on https://api.football-data.org 
Api_key = '295ebd7f84134205b84d083b5d5a26f6'

args = sys.argv[1:]

################## Default mode #############################################################
def default_function():
    # Scrapping from source 1
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
            print('Source unavailable. Check the internet connection')
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
    df_source1 = df_source1[['name', 'position', 'Age', 'Nat.', 'Market value', 'club']] 
    
    # Retrieve data by Api request from source 2
    # create connection with https://api.football-data.org
    # get competitions' id and name
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    try:
        connection.request('GET', '/v2/competitions/', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        p = response['competitions']
    except:
        print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
    competitions = pd.DataFrame()
    for item in p:
        competitions = competitions.append(item, ignore_index=True)
    competitions = competitions[['id', 'name', 'code']]
    competitions['id'] = competitions['id'].astype('int64')
    # We use 5 top european soccer ligues
    # Create a list of ids' of 5 top european soccer ligues
    listo = []
    kalisto = ['PL', 'BL1', 'SA', 'PD','FL1'] # code of 5 european soccer ligues (we can find from source 2)
    df = competitions.query("code == 'PL'")
    listo.append(df["id"].iloc[0])
    df = competitions.query("code == 'BL1'")
    listo.append(df["id"].iloc[0])
    df = competitions.query("code == 'SA'")
    listo.append(df["id"].iloc[0])
    df = competitions.query("code == 'PD'")
    listo.append(df["id"].iloc[0])
    df = competitions.query("code == 'FL1'")
    listo.append(df["id"].iloc[0])
    # get teams' id, name which participate in 5 top european soccer ligues
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    teams = pd.DataFrame()
    for i in listo:
        try:
            connection.request('GET', '/v2/competitions/' + str(i) + '/teams?season=2021', None, headers)
            response = json.loads(connection.getresponse().read().decode())
            p = response['teams']
            time.sleep(7)
        except:
            print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
        for item in p:
            teams = teams.append(item, ignore_index=True)
    teams = teams[['id', 'name']]
    teams['id'] = teams['id'].astype('int64')
    # list of clubs from source 1
    club_list = df_source1['club'].to_list()
    # matching list of clubs from source 1 with source 2
    club_df = teams[teams['name'].isin(club_list)]
    # we have 35 matches, for a simple analysis they are enough
    # get list of clubs' id
    id_clubs = club_df["id"].to_list()
    # get players' id, name which play for the clubs
    # we use time.sleep due to this api source has limitation 10 calls/minute
    # the data will be collected approximately 3-4 minutes 
    
    ######uncomment this section if you want to retrieve data from site########
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    players = pd.DataFrame()
    for i in id_clubs:
        try:
            connection.request('GET', '/v2/teams/' + str(i), None, headers)
            response = json.loads(connection.getresponse().read().decode())
            p = response['squad']
            time.sleep(7)
        except:
            print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
        for item in p:
            players = players.append(item, ignore_index=True)    
    players = players[['id', 'name']]
    players['id'] = players['id'].astype('int64')
    #####################end section###########################################
    
    ##########if you do not want to retrieve data again uncomment the row of code below########################
    # Read in the data set from source 1 to retrieve necessary player names
    # comment the code below if you have already used the section above
    #players = pd.read_csv('../data/players_api.csv')
    ###########################################################################
    
    # list of players from source 1
    player_list = df_source1['name'].to_list()
    # matching list of players from source 1 with source 2
    player_df = players[players['name'].isin(player_list)]
    # we have 202 matches, for a simple analysis they are enough
    # get list of players' id and list of player names
    #id_players = player_df["id"].to_list()
    name_players = player_df["name"].to_list()
    # we leave the players who matched
    df_source2 = df_source1[df_source1['name'].isin(name_players)]
    # we sort by name
    player_df = player_df.sort_values(by=['name'])
    df_source2 = df_source2.sort_values(by=['name'])
    # we add the "id" column from source2 into source1
    df_source2['id'] = player_df['id'].values
    # we get the number of wins, draws, and losts of players between 2021-08-01(start season) and 2021-11-23 (the day when we write this code)
    # we use time.sleep due to this api source has limitation 10 calls/minute
    # the data will be collected approximately 20 minutes
    ######uncomment this section if you want to retrieve data from site########
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    d = {}
    win_list = []
    draw_list = []
    lost_list = []
    match_result = pd.DataFrame()
    for i in df_source2['id'].values:
        try:
            connection.request('GET', '/v2/players/' + str(i) + '/matches?status=FINISHED&dateFrom=2021-08-01&dateTo=2021-11-23', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            a = df_source2[(df_source2['id'] == i)]
            p = response['matches']
            time.sleep(7)
        except:
            print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
        win = 0
        draw = 0
        lost = 0
        for t in p:
            s = t['score']
            h = t['homeTeam']
            nh = h['name']
            if nh in a['club'].values and s['winner'] == 'HOME_TEAM':
                win += 1
            elif s['winner'] == 'DRAW':
                draw += 1
            else:
                lost += 1
        win_list.append(win)
        draw_list.append(draw)
        lost_list.append(lost)
    d['win'] = win_list
    d['draw'] = draw_list
    d['lost'] = lost_list
    match_result = pd.DataFrame.from_dict(d)
    #####################end section###########################################
    
    ##########if you do not want to retrieve data again########################
    # Read in the data set from source 1 to retrieve necessary match results of players
    # comment the code below if you have already used the section above
    #match_result = pd.read_csv('../data/match_result.csv')
    ###########################################################################
    # we add 'win','draw','lost' columns into source1
    df_source2[['win','draw','lost']] = match_result[['win','draw','lost']].values
    print('Combined data from source 1 and source 2')
    print('Player statistics')
    print(df_source2)
    
    # Scrapping from source 3
    #load webpage https://www.theguardian.com
    # headers will be used to trick the website that we open it like a browser, not like a scrapping tool. 
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = 'https://www.theguardian.com/football/premierleague/table'
    try:
        content = requests.get(page, headers=headers)
    except:
        print('Source 3 unavailable. Check the internet connection')
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
        content = requests.get(page, headers=headers)
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
    df_source3['avg_points']=df_source3['Pts'] / df_source3['GP']
    # rename a column
    df_source3.rename(columns={'Team': 'club'}, inplace = True)
    print('data from source 3')
    print('Club statistics')
    print(df_source3)


######### Scrape mode ######################################################################
def scrape_function():
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
    df = pd.DataFrame(columns = columns)
    
    # Because of necessary data are divided into 20 webpages, we will use for loop  
    for i in range(1,2):
        page = 'https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&altersklasse=alle&ausrichtung=alle&jahrgang=0&kontinent_id=0&land_id=0&page=' + str(i) + '&plus=1&spielerposition_id=alle'
        content = requests.get(page, headers=headers)
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
            df_length = len(df)
            df.loc[df_length] = kalisto
    #print(kalisto)
    # dropping unnecessary columns
    df = df.drop(['delete1', 'delete2', 'delete3', 'delete4', 'delete5'], axis=1) 
    print('data from source 1')
    print('Most valuable soccer players from https://www.transfermarkt.us/ (Scrapping)')
    print(df.head())
    
    # get competitions' id and name
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    try:
        connection.request('GET', '/v2/competitions/', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        p = response['competitions']
    except:
        print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
    output = pd.DataFrame()
    for item in p:
        output = output.append(item, ignore_index=True)
    output = output[['id', 'name', 'code']]
    output['id'] = output['id'].astype('int64')
    # get list of id of 5 top european soccer ligues
    listo = []
    kalisto = ['PL', 'BL1', 'SA', 'PD','FL1'] # code of 5 european soccer ligues
    df = output.query("code == 'PL'")
    listo.append(df["id"].iloc[0])
    df = output.query("code == 'BL1'")
    listo.append(df["id"].iloc[0])
    df = output.query("code == 'SA'")
    listo.append(df["id"].iloc[0])
    df = output.query("code == 'PD'")
    listo.append(df["id"].iloc[0])
    df = output.query("code == 'FL1'")
    listo.append(df["id"].iloc[0])
    # get teams' id, name, and shortName
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': '295ebd7f84134205b84d083b5d5a26f6' }
    output = pd.DataFrame()
    for i in listo:
        try:
            connection.request('GET', '/v2/competitions/' + str(i) + '/teams?season=2021', None, headers)
            response = json.loads(connection.getresponse().read().decode())
            p = response['teams']
        except:
            print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
        for item in p:
            output = output.append(item, ignore_index=True)
    output = output[['id', 'name', 'shortName']]
    print('data from source 2')
    print('Soccer teams of 5 top european soccer ligues from api.football-data.org (Api request)')
    print(output.head())   

    # Scrapping from source 3
    #load webpage https://www.theguardian.com
    # headers will be used to trick the website that we open it like a browser, not like a scrapping tool. 
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = 'https://www.theguardian.com/football/premierleague/table'
    try:
        content = requests.get(page, headers=headers)
    except:
        print('Source 3 unavailable. Check the internet connection')
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
        content = requests.get(page, headers=headers)
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
    df_source3['avg_points']=df_source3['Pts'] / df_source3['GP']
    # rename a column
    df_source3.rename(columns={'Team': 'club'}, inplace = True)
    print('data from source 3')
    print('Club statistics')
    print(df_source3.head())

######### Static mode ######################################################################
def static_function(path_to_static_data):
    # Read in the data set from source 1 to retrieve necessary match results of players
    df = pd.read_csv(path_to_static_data)
    print('data from' + path_to_static_data)
    print(df.head())

###################command line######################

if len(sys.argv) == 1:
    #default mode
    default_function()
elif sys.argv[1] == '--scrape':
    #scrape mode
    #print a sample of the data you retrieve from your sources
    scrape_function()
elif sys.argv[1] == '--static':
    #static mode
    #print a sample of the static datasets you have built from your scraping
    path_to_static_data = sys.argv[2]
    static_function(path_to_static_data)





