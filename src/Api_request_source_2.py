#!/usr/bin/env python
# coding: utf-8

print('You have to wait more than 35 minutes to collect data from the internet')


#import necessary libraries
import http.client
import json
import pandas as pd
import time

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



