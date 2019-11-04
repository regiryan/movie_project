import requests
from bs4 import BeautifulSoup
import re
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
from datetime import datetime

# define year values for which you want the data
set_begin_year = 2009
set_end_year = 2019
list_of_years = list(range(set_begin_year, set_end_year+1))



# Function to pull for specified range of years, returns a list of pages, each page represents a list of rows from table of movies for that year
def get_all_year_tables(begin_year, end_year):
    all_year_tables = []
    # loop to iterate through years
    for year in range(begin_year, end_year+1):
        link = f'https://www.boxofficemojo.com/year/world/{year}/?ref_=bo_nb_di_tab'
        # get the raw data from linked webpage
        year_page = requests.get(link)
        # parse the webpage with beautiful soup
        year_soup = BeautifulSoup(year_page.content, 'html.parser')
        # isolate the table that contains the list of movies
        year_table = year_soup.find('div', attrs={'class': 'a-section imdb-scroll-table-inner'})
        # select all rows from the table of movies
        year_table_data = year_table.find_all('tr')
        # Remove title row
        year_table_data.remove(year_table_data[0])
        all_year_tables.append(year_table_data)
    print(f'This is a list with {len(range(begin_year, end_year+1))} webpages')
    return all_year_tables

# Call the function to get all tables
all_years_tables = get_all_year_tables(set_begin_year, set_end_year)


# function to iterate through a list of all pages/tables and return a list of lists of dicts of all values
def get_all_years_all_values(all_years_tables):
    all_years_all_values = []
    for table in all_years_tables:
        all_years_all_values.append(get_all_values_per_year(table))
    return all_years_all_values


# function that takes a table(an already isolated list of rows from the table of movies) and returns a list of dicts with all values
def get_all_values_per_year(year_table):
    # create a list container for all dictionaries
    all_values_per_year = []
    # for loop to iterate through each row in table
    for n in range(len(year_table)):
        movie_title = year_table[n].find('a', attrs={'class': 'a-link-normal'}).get_text()
        # returns 3 lines of html code containing the 3 box office values we need
        all_box_office_list_raw = year_table[n].find_all('td', attrs={'class': 'a-text-right mojo-field-type-money'})
        # create a container for 3 box office values, converted from string to int
        all_box_office_list_int = []
        # for loop to iterate through those 3 lines
        for each in all_box_office_list_raw:
            # get text from each line
            each_text = each.get_text()
            # print(each_text)
            # checks if values is empty, if yes converts to int, if not just renames it as each_int
            if each_text != '-':
                each_int = locale.atoi(each_text[1:])
            else:
                each_int = 'none'
            # appends each int value to list container created above
            all_box_office_list_int.append(each_int)
            # print(len(all_box_office_list_int))
            # creates a dictionary using the list of ints
        all_box_office_dict = dict(title=movie_title, worldwide=all_box_office_list_int[0], domestic=all_box_office_list_int[1], foreign=all_box_office_list_int[2])
            # appends each movie dict to a list container created above
        all_values_per_year.append(all_box_office_dict)
    return all_values_per_year


all_years_all_values = get_all_years_all_values(all_years_tables)



# takes in a list of pages (each page represents a list of rows from table of movies for that year), goes to individual
# pages for each movie and gets values. returns a list of dicts containing movie title, list of genres and release date
def get_page_values(all_years_tables):
    # create empty list container
    list_of_page_dicts = []
    # iterates throguh each year
    for n in range(len(all_years_tables)):
        # iterates throguh each row/movie
        for row in all_years_tables[n]:
            # create empty dict container
            page_values_dict={}
            # find the link to each individual page
            link_ref = row.find('a', attrs={'class': 'a-link-normal'})['href']
            # gets contents of that page and converts them to soup
            inner_page = requests.get(f'https://www.boxofficemojo.com{link_ref}')
            soup2 = BeautifulSoup(inner_page.content, 'html.parser')
            # finds the row that contains movie title
            movie_row = soup2.find('div', 'a-fixed-left-grid-col a-col-right')
            # gets the movie title
            movie_name = movie_row.find('h1', attrs={'class': 'a-size-extra-large'}).get_text()
            # adds a key-value pair to our dictionary containing movie title
            page_values_dict['title'] = movie_name
            # Finds the genres
            data_table = soup2.find('div', {'class' : 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
            for row in data_table:
                    text = row.text
                    if text.startswith('Genres'):
                        genres = text
                    else:
                        continue
            gen = genres.replace(' ','')
            stripped_gen = gen.replace('\n\n',',')
            genres_list = stripped_gen[6:].split(',')
            page_values_dict['genres'] = genres_list
            # gets release date
            date_row = data_table.find_all('a', attrs={'class': 'a-link-normal'})
            date = date_row[1].get_text()
            # attmepts to convert it to datetime (does not work well)
            clean_date = datetime.strptime(f'{date}', '%b %d, %Y')
            cleaner_date = clean_date.date()
            page_values_dict['release-date'] = cleaner_date
            list_of_page_dicts.append(page_values_dict)
    return list_of_page_dicts


# GETTING THE GENRES AND Stuff
# page_data = get_page_values(all_years_tables)


#
# all_years_tables[1]
#
# all_years_tables[0]
# ink_ref = all_years_tables[0][0].find('a', attrs={'class': 'a-link-normal'})['href']
#
# ink_ref
#
# ink_ref.split('/')[2]




# len(all_years_all_values)
#
# all_years_all_values[0][0]
#
#
# def add_year_values(list_of_years, all_years_all_values):
#     for n in range(len(all_years_all_values)):
#         for dict in all_years_all_values[n]:
#             set_year = list_of_years[n]
#             dict['year'] = set_year
#     return all_years_all_values
#
#
#
# final_all_years_all_values = add_year_values(list_of_years, all_years_all_values)
#
# final_all_years_all_values[0][0]
#
#
# # ____________________________________________________________
# def getall_tableyears(begin_year, end_year):
#     movie_list = []
#     for year in range(begin_year, end_year+1):
#         # print(year)
#         #reach out to the api for rottentomatoes
#         #first year is 2018
#         page = requests.get(f'https://www.rottentomatoes.com/top/bestofrt/?year={year}')
#         page
#         page.content
#         soup = BeautifulSoup(page.content, 'html.parser')
#         #test the soup connection
#         soup.get_text()
#
#         #get the data from the year's best movies
#         #access the table on the page
#         table_year = soup.find('table', attrs={'class': 'table'})
#         #access the informtion within the table
#         table_year_data = table_year.find_all('tr')
#         #parse the dataset
#
#         # remove the header row from the dataset
#         table_year_data.remove(table_year_data[0])
#         # print(table_year_data[0])
#         #parse the data
#         for index, movie in enumerate(table_year_data):
#             # #parse and select the rank to remove . from numbers
#             # rank = table_year_data[index].find('td', {'class': 'bold'}).text.strip().replace('.', '')
#             # #parse the find the name and remove blank spaces
#             # name = table_year_data[index].find('a', {'class': 'unstyled articleLink'}).text.strip()
#             # #remove the trailing year made into its own variables from the movie name
#             # year_made = int(name[-5:-1])
#             # name = name[0:(len(name) - 6)]
#             # name = name.strip()
#             # #parse the percent of each movie
#             # rt_percent = table_year_data[index].find('span', {'class': 'tMeterScore'}).text.strip()
#             # rt_percent_score = int(rt_percent.strip('%'))
#             # review_count = table_year_data[index].find('td', {'class': 'right hidden-xs'}).text
#             # #add each movie to a movie info list
#             # movie_info = []
#             # movie_info.extend([int(rank), name, rt_percent_score, year_made, int(review_count)])
#             # #turn each entry into a tuple
#             # movie_tuple = tuple(movie_info)
#             # movie_list.append(movie_tuple)
#
#             #dive one level deeper
#             link_ref = table_year_data[0].find('a', {'class': 'unstyled articleLink'})['href']
#             inner_page = requests.get(f'https://www.rottentomatoes.com{link_ref}')
#             soup2 = BeautifulSoup(inner_page.content, 'html.parser')
#             audience_score = soup2.find('span', {'class': 'mop-ratings-wrap__percentage'}).get_text().replace('%', '').strip()
#             user_ratings = list(soup2.find_all('strong', {'class': 'mop-ratings-wrap__text--small'}))
#             user_ratings_clean = (user_ratings[-1].text).split(':')
#             user_ratings_clean = int(user_ratings_clean[1].replace(',', '').strip())
#             #information table
#             # info_table = soup2.find('ul', {'class': 'content-meta info'})
#             # info_table2 = info_table.find_all('li', {'class': 'meta-row clearfix'})
#             # info_table3 = list(enumerate(info_table2))
#             print(user_ratings_clean)
#             break
#
# #
# type(all_years_tables[0])
# #
# all_years_tables[0]
# #
# def get_genres(all_years_tables):
#     list_of_genres_lists = []
#     for n in range(len(all_years_tables)):
#         for row in all_years_tables[n]:
#             link_ref = row.find('a', attrs={'class': 'a-link-normal'})['href']
#             inner_page = requests.get(f'https://www.boxofficemojo.com{link_ref}')
#             soup2 = BeautifulSoup(inner_page.content, 'html.parser')
#             movie_row = soup2.find('div', 'a-fixed-left-grid-col a-col-right')
#             movie_name = movie_row
#             data_table = soup2.find('div', {'class' : 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
#
#             # if len(data_table) != 8:
#             #     print('SOMETHING WENT WRONG, length of ')
#             # else:
#             #     continue
#             for row in data_table:
#                     text = row.text
#                     if text.startswith('Genres'):
#                         genres = text
#                     else:
#                         continue
#             genres
#             gen = genres.replace(' ','')
#             stripped_gen = gen.replace('\n\n',',')
#             genres_list = stripped_gen[6:].split(',')
#             list_of_genres_lists. append(genres_list)
#     return list_of_genres_lists
#
#
#
#
#
#     get_page_values(all_years_tables)
#
#
#
#
#
#
#     # Get the studio Name
#     for row in data_table:
#         text = row.text
#         if text.startswith('Distributor'):
#             studio = text
#         else:
#             continue
#
#
#
#
# # Testting
# link_ref = row.find('a', attrs={'class': 'a-link-normal'})['href']
# inner_page = requests.get(f'https://www.boxofficemojo.com{link_ref}')
# soup2
# soup2 = BeautifulSoup(inner_page.content, 'html.parser')
# # Finding the genres
# data_table = soup2.find('div', {'class' : 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
# for row in data_table:
#     text = row.text
#     if text.startswith('Distributor'):
#         studio = text
#         print(studio)
#     else:
#         continue
#
# data_table
# # Get release date
# date_row = data_table.find_all('a', attrs={'class': 'a-link-normal'})
# date = date_row[1].get_text()
# print(date)
#
#
#
#
#
#
#
# listt = []
# type(gen)
# for g in gen:
#     g.strip()
#     print(g)
#     listt.append(g)
#
#
#
# print(listt)
#
#     # spans = row.find('span')
#     for n in range(len(data_table)):
#         print(f'{n} - {row}')
#
# data_table[0].get_text()
#
# for row in data_table:
#     spans = row.find_all('span').group(0)
#     print(spans)
#
# all_divs = data_table[0].findall('div')
#
#
#
# print(type(data_table))
# data_table_contents = [data.get_text() for data in data_table]
# split_contents = data_table_contents[0].strip()
# pattern = re.compile(r'Genres(.*)Release')
#
# matches = pattern.finditer(split_contents)
# len(matches)
#
#
# matches2 = pattern.findall(split_contents)
# for match in matches:
#     print(match)
#
# print(split_contents)
# split_contents
#
#
#
# list_of_dicts = []
# for row in all_years_tables[0]:
#     page_values_dict={}
#     link_ref = row.find('a', attrs={'class': 'a-link-normal'})['href']
#     inner_page = requests.get(f'https://www.boxofficemojo.com{link_ref}')
#     soup2 = BeautifulSoup(inner_page.content, 'html.parser')
#     movie_row = soup2.find('div', 'a-fixed-left-grid-col a-col-right')
#     # Getting the movie title
#     movie_name = movie_row.find('h1', attrs={'class': 'a-size-extra-large'}).get_text()
#     page_values_dict['title'] = movie_name
#     # Finding the genres
#     data_table = soup2.find('div', {'class' : 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})
#     for row in data_table:
#             text = row.text
#             if text.startswith('Genres'):
#                 genres = text
#             else:
#                 continue
#     gen = genres.replace(' ','')
#     stripped_gen = gen.replace('\n\n',',')
#     genres_list = stripped_gen[6:].split(',')
#     page_values_dict['genres'] = genres_list
#     # Get release date
#     date_row = data_table.find_all('a', attrs={'class': 'a-link-normal'})
#     date = date_row[1].get_text()
#     page_values_dict['release-date'] = date
#     list_of_dicts.append(page_values_dict)
# print(list_of_dicts)
#
#
# # print(type(data_table_contents))
# # for span in data_table:
# #     print(span.find_all('span').contents)
# #
# # emails = '''
# # CoreyMSchafer@gmail.com
# # corey.schafer@university.edu
# # corey-321-schafer@my-work.net
# # '''
# #
# # pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
# #
# # matches = pattern.finditer(emails)
# #
# # for match in matches2:
# #     print(match)
# #
# #
# # for i in tqdm(test):
# #     driver.get(i)
# #     soup = BeautifulSoup(driver.page_source)
# #     try:
# #         table = soup.find_all('table')
# #         table_body=soup.find('tbody')
# #         rows = table_body.find_all('tr')
# #         watch_info = {}
# #         for row in rows:
# #             cols=row.find_all('td')
# #             cols= [x.text.strip() for x in cols]
# #             col1 = row.find_all('th')
# #             col1 = [x.text.strip() for x in col1]
# #             watch_info[str(col1)] = cols
# #         watch_info['price'] = (soup.find_all(name='span', class_ = 'price')[1].text)
# #         final_watch_info5.append(watch_info)
# #     except:
# #         print(i)
# #
# #     #rest
# #     sequence = [x/10 for x in range(8,15)]
# #     time.sleep(random.choice(sequence))
# # Collapse
# #
# # for i in tqdm(test):
# #     driver.get(i)
# #     soup = BeautifulSoup(driver.page_source)
# #     try:
# #         table = soup.find_all('table')
# #         table_body=soup.find('tbody')
# #         rows = table_body.find_all('tr')
# #         watch_info = {}
# #         for row in rows:
# #             cols=row.find_all('td')
# #             cols= [x.text.strip() for x in cols]
# #             col1 = row.find_all('th')
# #             col1 = [x.text.strip() for x in col1]
# #             watch_info[str(col1)] = cols
# #         watch_info['price'] = (soup.find_all(name='span', class_ = 'price')[1].text)
# #         final_watch_info5.append(watch_info)
# #     except:
# #         print(i)
# #
# #     #rest
# #     sequence = [x/10 for x in range(8,15)]
# #     time.sleep(random.choice(sequence))
# # Collapse
# #
# #
# #
# #
# #
# #
# #
# #
