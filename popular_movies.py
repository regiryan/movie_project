# setting up database
import requests
from bs4 import BeautifulSoup

#Outermost function

#update the year for each dataset that we want


#reach out to the api for rottentomatoes
#first year is 2018
page = requests.get("https://www.rottentomatoes.com/top/bestofrt/?year=2018")
page
page.content
soup = BeautifulSoup(page.content, 'html.parser')
#test the soup connection
soup.get_text()


#--------------------
#get the data from 2018's best movies


title2018 = soup.title

#access the table on the page
table2018 = soup.find('table', attrs={'class': 'table'})
#access the informtion within the table
table2018_data = table2018.find_all('tr')
table2018_data
type(table2018_data)


#---------
#parse the dataset


#remove the header row from the dataset
table2018_data[0]
table2018_data.remove(table2018_data[0])
table2018_data[0]
table2018_data

#parse the dataset
indiv_movie = list(table2018_data[0].children)
clean_list_element = []
len(indiv_movie)

indiv_movie.find_all('bs4.element.Tag')
#print(indiv_movie)
#indiv_movie[5]
[print(type(movie)) for movie in indiv_movie]
for movie in indiv_movie:
    print(movie)

for item in indiv_movie:
    try:
        c_text = indiv_movie.get_text()
        clean_list_element.append(c_text)
    except:
        pass

clean_list_element = []

#column headers
best_rt_movies_headers = list(table2018_data[0].children)

rt_movie_headers = ['Rank', 'Tomatometer Rating', 'Title', 'No. of Reviews']
