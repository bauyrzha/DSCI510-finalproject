# DSCI510-finalproject
hw5 the final project


DSCI 510 Fall - Final project description 
1. The name of the student:
	Yerkebulan Bauyrzhanov (only one)

2. About the project:
	Analysis I would like to do with the combined data is to find:
1)	What affects the transfer cost of a soccer player?
2)	Do top players (superstars) influence the results of the match? If yes, how do they influence it? 
I will get data from sources, clean them if needed, make some hypothesizes (predictions), and visualize the results. 

3. Datasources:

Source 1 = https://www.transfermarkt.us/ - one of the biggest soccer databases and communities in the world. 
We will get information about the most valuable players by web-scrapping. 

Source 2 = https://api.football-data.org - External public API, provides football data and statistics 
(live scores, fixtures, tables, squads, lineups/subs, etc.) in a machine-readable way.
We will get information about players, their results of the matches by API requests.

Source 3 = https://www.theguardian.com/football - the part of news-portal about soccer with current standings of soccer clubs.  
We will get information about soccer clubs in 5 top European soccer leagues by web-scrapping.

4. Information about API keys for Source 2:
You have to register to receive an API key by email. The free API key has limitations. 
You will be available to send no more than 10 requests in a minute. 

5. Requirements:
Unzip \data and \src from the zip file in one directory. I use python version 3.8. 'scraper.py' script is located in the src folder. static data is located in the data folder.
Please check out requirements.txt to know about requirements according to software.

6. A drawing (Entity Relationship Diagram):
Look drawing.png to find out what objects/items will be extracted from the data sources and what they will be combined into.  

7. How to run scraper.py from the command line:
Run command line from src folder.
scraper.py has three modes of running.
a) default mode: 
command: python .\scraper.py
purpose: scrape ALL of the data and print it in a useful way.
result: print 5 rows of the table with combined data from sources 1 and 2.
		print 5 rows of the table with data from source 3.
Be ready that it takes more than 25 minutes to scrape datasets from sources due to the API source having a limitation of 10 calls/minute.
Note1: Although I use a timeout in my code, you might catch an error. Wait for the script to finish.
       I am advising do not to run the script in different modes in parallel or immediately one after the other.
Note2: If you do not want to retrieve data again uncomment the row of code that just export data from CSV file. 
	   You will figure out it by reading comments in the script.
	   
b) scrape mode:
command: python .\scraper.py --scrape
purpose: scrape SOME of the data (just as an example) 
result: print 5 rows of the table 'Most valuable soccer players from source 1 (Scrapping)'.
		print 5 rows of the table 'Soccer teams of 5 top European soccer leagues from source 2 (Api request)'.
		print 5 rows of the table 'Club statistics from source 3'.

c) static mode:
command: python .\scraper.py --static ..\data\{name_of_file}
purpose: open and print the static copies of your data
result: print 5 rows from {name_of_file}.
Note: the files with data in CSV format are located in the data folder. 

9. Description of files
To find out the whole usage, check out Yerkebulan_Bauyrzhanov_project_description.pdf.

8. Analysis step:
to show plots run /src/Yerkebulan_Bauyrzhanov.py from command line or /src/Yerkebulan_Bauyrzhanov.ipynb from jupiter notebook.
