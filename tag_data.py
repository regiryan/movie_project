import pandas as pd
import numpy
import csv
import mysql.connector
import config
# import boxmojo as box

cnx = mysql.connector.connect(
    host=config.host,
    user=config.user,
    passwd=config.password,
    database='movie_project'
    )


cursor = cnx.cursor()
cursor
# create tag tags table
column_headers_tags = ['tag_id', 'tag', 'tag_popularity']

TABLES = {}

TABLES['tags'] = ("""CREATE TABLE tags
                (tag_id VARCHAR(255) NOT NULL PRIMARY KEY,
                tag VARCHAR(255) NOT NULL,
                tag_popularity VARCHAR(255) NOT NULL)
                ENGINE = InnoDB ;
                """)

TABLES['tag_relevance'] = ("""CREATE TABLE tag_relevance
                (movie_id VARCHAR(255) NOT NULL PRIMARY KEY,
                tag_id VARCHAR(255) NOT NULL,
                tag_relevance FLOAT NOT NULL)
                ENGINE = InnoDB ;
                """)

TABLES['movie_tags'] = ("""CREATE TABLE movie_tags
                (movie_id VARCHAR(255) NOT NULL PRIMARY KEY,
                movie_title VARCHAR(255) NOT NULL,
                movie_popularity VARCHAR(255) NOT NULL)
                ENGINE = InnoDB ;
                """)



cursor.execute(TABLES['movie_tags'])
cursor.execute(TABLES['tag_relevance'])
cursor.execute(TABLES['tags'])




alter_tag_relevance = """ALTER TABLE tag_relevance
                        ADD FOREIGN KEY (tag_id) REFERENCES tags(tag_id);"""
cursor.execute(alter_tag_relevance)

alter_movie_tags = """ALTER TABLE movie_tags
                        DROP FOREIGN KEY (movie_id) REFERENCES tag_relevance(movie_id);"""
cursor.execute(alter_movie_tags)

# tag_data = read_table(tags.dat, "  ")

list_of_tag_tuples = []
with open('tags.dat', newline = '') as tags:
	tag_reader = csv.reader(tags, delimiter='\t')
	for tag in tag_reader:
		list_of_tag_tuples.append(tag)
list_of_tag_tuples

list_of_tag_rel_tuples = []
with open('tag_relevance.dat', newline = '') as tags:
	tag_reader = csv.reader(tags, delimiter='\t')
	for tag in tag_reader:
		list_of_tag_rel_tuples.append(tuple(tag))
list_of_tag_rel_tuples


list_of_movie_tags_tuples = []
with open('movies.dat', newline = '') as tags:
	tag_reader = csv.reader(tags, delimiter='\t')
	for tag in tag_reader:
		list_of_movie_tags_tuples.append(tuple(tag))
list_of_movie_tags_tuples



add_tag_data = """INSERT INTO tags
        (tag_id, tag, tag_popularity)
        VALUES (%s, %s, %s)"""
cursor.executemany(add_tag_data, list_of_tag_tuples)
 cnx.commit()

print(len(list_of_tag_rel_tuples))
add_tag_rel_data = """INSERT INTO tag_relevance
        (movie_id, tag_id, tag_relevance)
        VALUES (%s, %s, %s)"""
cursor.executemany(add_tag_rel_data, list_of_tag_rel_tuples)
cnx.commit()

add_movie_tag_data = """INSERT INTO movie_tags
        (movie_id, movie_title, movie_popularity)
        VALUES (%s, %s, %s)"""
cursor.executemany(add_movie_tag_data, list_of_movie_tags_tuples)
cnx.commit()
cnx.close()
