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

# Read in the data sets
df = pd.read_csv('../data/df_source1+source2.csv')
df3 = pd.read_csv('../data/df_source3.csv')

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

# In[7]:


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
