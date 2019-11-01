# setting up database
import requests
from bs4 import BeautifulSoup
import time
import mysql.connector
import config
import csv

#Outermost function
#rotten tomatoes data scrapper

#update the year for each dataset that we want
def getall_tableyears(begin_year, end_year):
    movie_list = []
    for year in range(begin_year, end_year + 1):
        #reach out to the api for rottentomatoes
        #first year is 2018
        page = requests.get(f'https://www.rottentomatoes.com/top/bestofrt/?year={year}')
        page
        page.content
        soup = BeautifulSoup(page.content, 'html.parser')
        #test the soup connection
        soup.get_text()

        #get the data from the year's best movies
        #access the table on the page
        table_year = soup.find('table', attrs={'class': 'table'})
        #access the informtion within the table
        table_year_data = table_year.find_all('tr')
        #parse the dataset

        # remove the header row from the dataset
        table_year_data.remove(table_year_data[0])
        #parse the data
        for index, movie in enumerate(table_year_data):
            #parse and select the rank to remove . from numbers
            rank = table_year_data[index].find('td', {'class': 'bold'}).text.strip().replace('.', '')
            #parse the find the name and remove blank spaces
            name = table_year_data[index].find('a', {'class': 'unstyled articleLink'}).text.strip()
            #remove the trailing year made into its own variables from the movie name
            year_made = int(name[-5:-1])
            name = name[0:(len(name) - 6)]
            name = name.strip()
            #parse the percent of each movie
            rt_percent = table_year_data[index].find('span', {'class': 'tMeterScore'}).text.strip()
            rt_percent_score = int(rt_percent.strip('%'))
            review_count = table_year_data[index].find('td', {'class': 'right hidden-xs'}).text
            #go one level lower
            link_ref = table_year_data[index].find('a', {'class': 'unstyled articleLink'})['href']
            inner_page = requests.get(f'https://www.rottentomatoes.com{link_ref}')
            soup2 = BeautifulSoup(inner_page.content, 'html.parser')
            #get the audience_score for each movie
            audience_score = soup2.find('span', {'class': 'mop-ratings-wrap__percentage'}).get_text().replace('%', '').strip()
            #get the number of user reviews
            user_ratings = list(soup2.find_all('strong', {'class': 'mop-ratings-wrap__text--small'}))
            user_ratings_clean = (user_ratings[-1].text).split(':')
            user_ratings_clean = user_ratings_clean[1].replace(',', '').strip()
            #add each movie to a movie info list
            movie_info = []
            movie_info.extend([int(rank), name, rt_percent_score, year_made, int(review_count), int(audience_score), user_ratings_clean])
            #turn each entry into a tuple
            movie_tuple = tuple(movie_info)
            movie_list.append(movie_tuple)
            #wait for 1 second before repeating the process
            time.sleep(.3)

    return movie_list

#call the function with years
best_past_decade_movies = getall_tableyears(2009, 2019)

best_past_decade_movies

#----------------------
#creating tables and inserting data

column_headers = ['ranking', 'title', 'tomatometer_rating', 'year', 'no_reviews', 'audience_score', 'user_ratings']

cnx = mysql.connector.connect(
    host=config.host,
    user=config.user,
    passwd=config.password,
    database='movie_project'
)
#testing database connection
print(cnx)

cursor = cnx.cursor()

#creating TABLES
DB_NAME = 'movie_project'

TABLES = {}

TABLES['decades_best_movies'] = ("""CREATE TABLE decades_best_movies
                                (ranking int(11) NOT NULL,
                                title varchar (90) NOT NULL,
                                tomatometer_rating int(11) NOT NULL,
                                year int(11) NOT NULL,
                                no_reviews int(11) NOT NULL,
                                audience_score int(11) NOT NULL,
                                user_ratings varchar(90) NOT NULL)
                                ENGINE=InnoDB ;
                                """)

TABLES['decades_best_movies']

#create the table
cursor.execute(TABLES['decades_best_movies'])

#drop the table
cursor.execute("""DROP TABLE decades_best_movies""")

cursor.close()
cnx.close()

#inserting data into databade ----------------------------
cnx = mysql.connector.connect(
    host=config.host,
    user=config.user,
    passwd=config.password,
    database='movie_project'
)

cursor = cnx.cursor()

movies_stmt = """INSERT INTO decades_best_movies
 (ranking, title, tomatometer_rating, year, no_reviews, audience_score, user_ratings)
  VALUES (%s, %s, %s, %s, %s, %s, %s)"""

for entry in best_past_decade_movies:
    print(entry)
    cursor.execute(movies_stmt, entry)
cnx.commit()
cursor.close()

#create box office mojo table -------------------------------------
TABLES['box_office_mojo'] = ("""CREATE TABLE box_office_mojo
                                (title varchar(255) NOT NULL,
                                worldwide_rev int (90) NOT NULL,
                                domestic_rev int(90) NOT NULL,
                                foreign_rev int(11) NOT NULL)
                                ENGINE=InnoDB ;
                                """)

cnx = mysql.connector.connect(
    host=config.host,
    user=config.user,
    passwd=config.password,
    database='movie_project'
)

cursor = cnx.cursor()

cursor.execute(TABLES['box_office_mojo'])
cursor.close()
cnx.close()

#--------------------------------------------
