#!/usr/bin/env python
# coding: utf-8

# ### DSCI 510 Fall 2021 Final Project Submission

# 1.	**The name of student**:
# 
#     Yerkebulan Bauyrzhanov

# 2. **About the project (Motivation):**
# 
#     I am a fan of soccer. Therefore, I decided to choose this topic as my fist data analysis project.
#     Analysis I would like to do with the combined data is to find:
#     
#     1)	What affects the transfer cost of a soccer player? For example, does the number of goals affect the transfer cost of a soccer player?
#     
#     2)	Do players with a high market value influence the results of the match?

# 3. **Datasources:**
# 
# **Source 1** = https://www.transfermarkt.us/ - one of the biggest soccer databases and communities in the world. 
# We will get information about the most valuable players by web-scrapping.
# 
# **Source 2** = https://api.football-data.org - External public API, provides football data and statistics 
# (live scores, fixtures, tables, squads, lineups/subs, etc.) in a machine-readable way.
# We will get information about players, their results of the matches by API requests.
# 
# **Source 3** = https://www.theguardian.com/football - the part of news-portal about soccer with current standings of soccer clubs. 
# We will get information about soccer clubs in 5 top European soccer leagues by web-scrapping.

# 4. **Information about API keys for Source 2:**
# 
# We have to register to receive an API key by email. The free API key has limitations. 
# We will be available to send no more than 10 requests in a minute.

# 5. **How to run the code**
# 
# We can get the clean data used in this notebook analysis simply from the data subfolder where the data sets have existed already, or you can run the data_collector.py file to get the data sets from the Internet.
# 
# To do so, using command-line: python .\src\data_collector.py, then datasets will be stored in the data subfolder.
# 
# Be ready that it takes more than 25 minutes to scrape datasets from sources (especially source2) due to the API source having a limitation of 10 calls/minute.
# 
# This project requires the following packages:
# 
# pandas, numpy, seaborn, requests, and beautifulsoup To run this project, make sure the above packages are installed, and then simply clone the repo at https://github.com/bauyrzha/DSCI510-finalproject and execute this notebook.
# 
# If it cannot successfully run, check the requirements.txt.
# 
# We can also collect data from sources separately by running Scrapping_source_1.py, Api_request_source_2.py, and Scrapping_source_3.py. 

# # Analysis performed for combained data sources 1 and 2
# 
# 1) Before analyzing let's find out what variables we have.
# 
# **name** - name of players.
# 
# **position** - position of players on the soccer pitch.
# 
# **Age** - age of players.
# 
# **Nat.** - nationality of players.
# 
# **Market value** - the cost of players in the transfer market.
# 
# **club** - the name of clubs where players are playing.
# 
# **Goals** - the number of goals of players in the current season (2021-2022).
# 
# **Assists** - the number of assists of players in the current season (2021-2022).
# 
# **win** - the number of wins in the current season (2021-2022).
# 
# **draw** - the number of draws in the current season (2021-2022).
# 
# **lost** - the number of losses in the current season (2021-2022).

# 6. **Сreate new variables that will be needed for analysis.**
# 
# Below the following variables will be created:
# 
# **player_avg_points** - the average earned points of players in one match in the current season (2021-2022).
# 
# **continent** - we divided players into two categories: players who are from European countries and who are from other (non-Europe countries)
# 




#import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import requests
import sys
import http.client
import json
import time
import os

args = sys.argv[1:]


def scrape_analysis():

    print('it takes more than 35 minutes to scrape datasets from the internet')
    
    
    ##############################################################Source1#############################################################################
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
    
    path = '../data'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
  
    # Create a new directory because it does not exist 
        os.makedirs(path)
        
    print("The new directory is created!")
    
    # export our data into csv file.
    df_source1.to_csv('../data/df_source1.csv', index=False)
    print("df_source1 is exported to '../data/df_source1.csv'")
    
    ############################################################################Source2################################################################
    
    #my api_key. You will receive your own if you register on https://api.football-data.org 
    Api_key = '295ebd7f84134205b84d083b5d5a26f6'
    
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
    competitions
    
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
        time.sleep(8)
        try:
            connection.request('GET', '/v2/competitions/' + str(i) + '/teams?season=2021', None, headers)
            response = json.loads(connection.getresponse().read().decode())
            p = response['teams']
        except:
            print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
        for item in p:
            teams = teams.append(item, ignore_index=True)
    teams = teams[['id', 'name']]
    teams['id'] = teams['id'].astype('int64')
    #teams.info()
    
    # Read in the data set from source 1 to retrieve necessary club names
    df_source1 = pd.read_csv('../data/df_source1.csv')
    
    # checking our DataFrame
    #df_source1.info()
    
    # list of clubs from source 1
    club_list = df_source1['club'].to_list()
    #print(club_list)
    
    # matching list of clubs from source 1 with source 2
    club_df = teams[teams['name'].isin(club_list)]
    #club_df.info()
    
    # we have 35 matches, for a simple analysis they are enough
    # get list of clubs' id
    id_clubs = club_df["id"].to_list()
    #print(id_clubs)
    
    #timeout
    time.sleep(8)
    
    # get players' id, name which play for the clubs
    # we use time.sleep due to this api source has limitation 10 calls/minute
    # the data will be collected approximately 3-4 minutes
    # If you do not want to wait, we can import already collected data from csv file, just uncomment the code (the cell) below
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    players = pd.DataFrame()
    for i in id_clubs:
        time.sleep(8)
        try:
            connection.request('GET', '/v2/teams/' + str(i), None, headers)
            response = json.loads(connection.getresponse().read().decode())
            p = response['squad']
        except:
            print('Source 2 unavailable or you reached the maximum request in particular time. You must not request more often than 10 calls/minute. Check the internet connection or Api key')
        for item in p:
            players = players.append(item, ignore_index=True)   
    players = players[['id', 'name']]
    players['id'] = players['id'].astype('int64')
    #players.info()
    
    # Read in the data set from source 1 to retrieve necessary player names
    #players = pd.read_csv('../data/players_api.csv')
    
    # export our data into csv file.
    players.to_csv('../data/players_api.csv', index=False)
    
    # list of players from source 1
    player_list = df_source1['name'].to_list()
    
    # matching list of players from source 1 with source 2
    player_df = players[players['name'].isin(player_list)]
    #player_df.info()
    
    # we have 202 matches, for a simple analysis they are enough
    # get list of players' id and list of player names
    id_players = player_df["id"].to_list()
    name_players = player_df["name"].to_list()
    
    # we leave the players who matched
    df_source2 = df_source1[df_source1['name'].isin(name_players)]
    #df_source2.info()
    
    # we sort by name
    player_df = player_df.sort_values(by=['name'])
    df_source2 = df_source2.sort_values(by=['name'])
    
    # we add the "id" column from source2 into source1
    df_source2['id'] = player_df['id'].values
    
    # checking our DataFrame
    #df_source2.info()
    
    #timeout
    time.sleep(8)
    # we get the number of wins, draws, and losts of players between 2021-08-01(start season) and 2021-11-23 (the day when we write this code)
    # we use time.sleep due to this api source has limitation 10 calls/minute
    # the data will be collected approximately 20 minutes
    # If you do not want to wait, we can import already collected data from csv file, just uncomment the code (the cell) below
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': Api_key }
    d = {}
    win_list = []
    draw_list = []
    lost_list = []
    match_result = pd.DataFrame()
    for i in df_source2['id'].values:
        time.sleep(8)
        try:
            connection.request('GET', '/v2/players/' + str(i) + '/matches?status=FINISHED&dateFrom=2021-08-01&dateTo=2021-11-23', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            a = df_source2[(df_source2['id'] == i)]
            p = response['matches']
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
    #match_result   
    
    # Read in the data set from source 1 to retrieve necessary match results of players
    #match_result = pd.read_csv('../data/match_result.csv')
    
    # export our data into csv file.
    match_result.to_csv('../data/match_result.csv', index=False)
    
    # we add 'win','draw','lost' columns into source1
    df_source2[['win','draw','lost']] = match_result[['win','draw','lost']].values
    
    # checking our DataFrame
    #df_source2
    
    # export our data into csv file.
    df_source2.to_csv('../data/df_source1+source2.csv', index=False)
    print("df_source2 is exported to '../data/df_source1+source2.csv'")
    
    #####################################################################Source3#############################################################################
    
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

def static_analysis():
    
    try:    
        # Read in the data sets
        df = pd.read_csv('../data/df_source1+source2.csv')
        df3 = pd.read_csv('../data/df_source3.csv')
        print('Static data are founded')
    except:
        print('Static data could not be founded')
        print('Start collecting data from the internet')
        scrape_analysis()  
        # Read in the data sets
        df = pd.read_csv('../data/df_source1+source2.csv')
        df3 = pd.read_csv('../data/df_source3.csv')
        print('Static data are founded')
    
    # get unique nationalities of players
    df['Nat.'].unique()
    
    # I want to add a new variable 'continent' which we divided players into two categories: 
    # players who are from European countries and who are from other (non-Europe countries)
    nat_list = ['England', 'France', 'Italy', 'Belgium', 'Spain', 'Denmark', 'Scotland', 'Portugal','Germany', 'Netherlands', 'Albania', 'Austria', 'Sweden', 'Switzerland', 'Hungary', 'Norway', 'Turkey', 'Czech Republic', 'Ukraine', 'Serbia']
    df['continent'] = np.where(df['Nat.'].isin(nat_list), 'Europe', 'other')
    
    #add a new column player_points (average points in one match)
    df['player_avg_points'] = (df['win']*3 + df['draw'])/(df['win'] + df['draw'] + df['lost'])
    
    # check our DataFrame
    df.info()
    
    
    # 7. **Data cleaning**
    # 
    # We will
    # 
    # - delete extra characters
    # 
    # - change type of variables
    # 
    # - delete NaN rows in continuous variables 
    # 
    # - delete the column 'id'
    
    
    # replace a character from column to apply to numeric
    df['Market value'] = df['Market value'].str.replace('m','')
    df['Market value'] = df['Market value'].str.replace('£','')
    
    
    df.head()
    
    
    # change type of the column
    df['Market value'] = df['Market value'].astype('float') 
    
    
    # check our DataFrame
    df.info()
    
    # delete error data in our dataFrame
    df = df.dropna()
    
    # check our DataFrame
    df.info()
    
    #delete the column 'id'
    df = df.drop('id', axis = 1)
    
    
    df.info()
    
    
    # # Data visualization
    # 
    # We use visualization to "grab" some hypotheses (predictions) on our data.
    # 
    # In our particular case, we want to establish the following: 
    # 
    # 1) the distribution of the target variable - the market value (cost); 
    # 
    # 2) presence of correlation between variables. 
    
    # 8. **Figure out the distribution of the target variable**
    
    #Trying to figure out the distribution of the market value (cost);
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # the line is the density of the distribution
    
    sns.histplot(df['Market value'], kde=True) 
    plt.title('Market value distribution')
    
    
    # We see that there is no normal distribution because, in the intervals 15 - 30 and 55 - 60, we see the rise of the lines. This should not be the case with the normal distribution. This means that we observe costs in these intervals more often than the normal distribution predicts. 
    
    # 9. **Figure out correlation between variables**
    
    # a) Market value, age and continent
    
    # Set the style of the graph
    sns.set_theme(color_codes=True)
    
    # set the size of the graph
    fig, ax = plt.subplots(figsize=(15, 10)) 
    
    #Trying to figure out whether the market value correlates the Ages
    sns.regplot(x='Age', y='Market value', data = df, scatter_kws={'s':80, 'alpha': 0.3}) 
    
    # Get the R squared value
    df['Market value'].corr(df['Age'])
    
    
    # We can conclude that the Market value and age of players have a slight negative relationship.
    # R squared value is close to zero, which can be considered no relationship.
    
    # linear regression with the third variable, which is given by color
    # In our case, we use 'continent' as the third variable.
    
    sns.lmplot(x='Age', y='Market value', hue="continent", data=df, markers=["o", "x"], palette="Set1")
    plt.title('linear regression with the third variable')
    
    
    # In this plot, we can consider that players from Europe lose the market value with age whereas players from non-European countries become more expensive. 
    
    # b) Market value, Goals and continent
    
    # Set the style of the graph
    sns.set_theme(color_codes=True)
    
    # set the size of the graph
    fig, ax = plt.subplots(figsize=(15, 10)) 
    
    #Trying to figure out whether the market value correlates the Goals
    sns.regplot(x='Goals', y='Market value', data = df, scatter_kws={'s':80, 'alpha': 0.3}) 
    
    # Get the R squared value
    df['Market value'].corr(df['Goals'])
    
    
    # We can conclude that the Market value and the number of goals of players have a enough strong relationship. That is, it means the more goals players score, the higher their market value is. 
    
    # linear regression with the third variable, which is given by color
    # In our case, we use 'continent' as the third variable.
    
    sns.lmplot(x='Goals', y='Market value', hue="continent", data=df, markers=["o", "x"], palette="Set1")
    plt.title('linear regression with the third variable')
    
    
    # c) Market value, Assists and continent
    
    # Set the style of the graph
    sns.set_theme(color_codes=True)
    
    # set the size of the graph
    fig, ax = plt.subplots(figsize=(15, 10)) 
    
    #Trying to figure out whether the market value correlates the Assists
    sns.regplot(x='Assists', y='Market value', data = df, scatter_kws={'s':80, 'alpha': 0.3}) 
    
    # Get the R squared value
    df['Market value'].corr(df['Assists'])
    
    
    # We can conclude that the Market value and the number of assists of players have a relationship, but not stronger than goals. That is, it means the more assists players do, the higher their market value is. 
    
    # linear regression with the third variable, which is given by color
    # In our case, we use 'continent' as the third variable.
    
    sns.lmplot(x='Assists', y='Market value', hue="continent", data=df, markers=["o", "x"], palette="Set1")
    plt.title('linear regression with the third variable')
    
    
    # d) Market value, player_avg_points and continent
    
    # Set the style of the graph
    sns.set_theme(color_codes=True)
    
    # set the size of the graph
    fig, ax = plt.subplots(figsize=(15, 10)) 
    
    #Trying to figure out whether the market value correlates the player_points
    sns.regplot(x='player_avg_points', y='Market value', data = df, scatter_kws={'s':80, 'alpha': 0.3}) 
    
    # Get the R squared value
    df['Market value'].corr(df['player_avg_points'])
    
    
    # We can conclude that the Market value and player_points have a slight positive relationship. That is, it means The more points players earn, the higher their price is.
    
    
    # linear regression with the third variable, which is given by color
    # In our case, we use 'continent' as the third variable.
    
    sns.lmplot(x='player_avg_points', y='Market value', hue="continent", data=df, markers=["o", "x"], palette="Set1")
    plt.title('linear regression with the third variable')
    
    
    # # The number of goals, the number of assists, and points players earn affect the transfer cost of a soccer player.
    
    # # Analysis performed for combained data sources 1, 2 and 3
    #  
    # 1) Before analyzing let's find out what variables we have.
    # 
    # **club** - the name of clubs where players are playing.
    # 
    # **Age** - the average age of players grouped by the club.
    # 
    # **Market value** - the average cost of players grouped by the club in the transfer market.
    # 
    # **Goals** - the average number of goals of players grouped by the club in the current season (2021-2022).
    # 
    # **Assists** - the average number of assists of players grouped by the club in the current season (2021-2022).
    # 
    # **win** - the average number of wins of players grouped by the club in the current season (2021-2022).
    # 
    # **draw** - the average number of draws of players grouped by the club in the current season (2021-2022).
    # 
    # **lost** - the average  number of losses of players grouped by the club in the current season (2021-2022).
    # 
    # **club_avg_points** - the average earned points of clubs in one match in the current season (2021-2022). 
    
    # Read in the data set (data source 3)
    df3 = pd.read_csv('../data/df_source3.csv')
    
    # delete extra character for matching with source 3
    extra_characters = [' FC','FC ', ' BC', 'AC ', ' CF', 'AC ', 'AS ', 'SS ', 'SSC ', 'ACF ']
    for ch in extra_characters:
        df['club'] = df['club'].str.replace(ch, '')
    
    # Get the average of all continuous variables for each club
    df2 = df.groupby(df['club']).mean()
    
    # reset index
    df2 = df2.reset_index()
    
    #check our dataframe
    df2.info()
    
    # get list of clubs
    club_list = df2["club"].to_list()
    print(club_list)
    
    # we leave the clubs which matched
    df3 = df3[df3['club'].isin(club_list)]
    
    df3.info()
    
    # we have 22 clubs, for simple analysis it is enough.
    # get list of clubs
    club_list = df3["club"].to_list()
    print(club_list)
    
    # we leave the clubs which matched
    df2 = df2[df2['club'].isin(club_list)]
    
    #check our dataFrame
    df2.info()
    
    # we sort by name of clubs in data source 3
    df3 = df3.sort_values(by=['club'])
    
    #check our dataFrame
    df3
    
    # we add the "club_avg_points" column from source2 into source1
    df2['club_avg_points'] = df3['club_avg_points'].values
    
    #check our dataframe
    df2.info()
    
    
    # 10. **Figure out correlation between between market value and club_avg_points**
    
    # Set the style of the graph
    sns.set_theme(color_codes=True)
    
    # set the size of the graph
    fig, ax = plt.subplots(figsize=(15, 10)) 
    
    #Trying to figure out whether the market value correlates the player_points
    sns.regplot(x='Market value', y='club_avg_points', data = df2, scatter_kws={'s':80, 'alpha': 0.3}) 
    
    # Get the R squared value
    df2['club_avg_points'].corr(df2['Market value'])
    
    plt.show()
    # We can conclude that the club_points and Market value have a good positive relationship. This means that the more high value players play in the club, the more points the club earns.
    
    # # Conclusion
    
    # We scraped data from three different resources.
    # 
    # We combined them.
    # 
    # We added new variables for analysis.
    # 
    # We did cleaning steps.
    # 
    # We did the analysis and, according to the figures and R squared values, we concluded that:
    # 
    # 1) **The number of goals, the number of assists, and points players earn affect the transfer cost of a soccer player.**
    # 
    # 2) **The Market value and age of players have a slight negative relationship. R squared value is close to zero, which can be considered no relationship. However, we can consider that players from Europe lose the market value with age whereas players from non-European countries become more expensive.**
    # 
    # 3) **The more high-value players play in the club, the more points the club earns. That means players with a high market value influence the results of the match.**
    
    
###################command line######################

if len(sys.argv) == 1:
    scrape_analysis()
    static_analysis()
elif sys.argv[1] == '--static':
    static_analysis()