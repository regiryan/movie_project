
import popular_movies as pm
# Connecting to the database
# connecting to the database using 'connect()' method
# it takes 3 required parameters 'host', 'user', 'passwd'

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

for entry in pm.best_past_decade_movies:
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
