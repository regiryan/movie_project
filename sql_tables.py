import mysql.connector
import config
import boxmojo as box
# Connecting to the database
# connecting to the database using 'connect()' method
# it takes 3 required parameters 'host', 'user', 'passwd'

# column_headers = ['title', 'title', 'tomatometer_rating', 'year', 'no_reviews']

cnx = mysql.connector.connect(
    host=config.host,
    user=config.user,
    passwd=config.password,
    database='movie_project'
    )

cursor = cnx.cursor()

#creating TABLES
# DB_NAME = 'movie_project'

add_box_data = """INSERT INTO box_office_mojo
 (title, worldwide_rev, domestic_rev, foreign_rev, year)
 VALUES (%(title)s, %(worldwide)s, %(domestic)s, %(foreign)s, %(year)s)"""

# box.final_all_year_all_values[0][0].keys()
 #
 # cursor.executemany(movies_stmt, pm.best_past_decade_movies)
 # cnx.commit()
 # cursor.close()


# dict_keys(['title', 'worldwide', 'domestic', 'foreign', 'year'])

for year in box.final_all_years_all_values:
    cursor.executemany(add_box_data, year)

cnx.commit()
