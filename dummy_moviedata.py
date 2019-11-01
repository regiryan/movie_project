import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pylab as plt
import statistics

data = pd.read_csv('IMDB-Movie-Data.csv')

data

#there are 128 null values for revenue, so we drop the null values
data = pd.DataFrame(data)
len(data)
data.dropna(axis=0, inplace=True)
data.reset_index()

#filtered revenues
filtered_rev = more_profitable_films['Revenue (Millions)']
filtered_meta = more_profitable_films['Metascore']
filtered_rating = more_profitable_films['Rating']

#calculating the iqr
deviation_rev = statistics.stdev(more_profitable_films['Revenue (Millions)'])
med_rev =  statistics.median(more_profitable_films['Revenue (Millions)'])
mean_rev = statistics.mean(more_profitable_films['Revenue (Millions)'])
mean_rev
deviation_rev
med_rev
len(filtered_rev)
len(filtered_meta)

#spliting the IQR into two so we can
zone = deviation_rev/2
up_bound = mean_rev + zone

low_bound = mean_rev - zone

more_profitable_films = []
#remove the outlier situations
more_profitable_films = data[(data["Revenue (Millions)"] > low_bound) & (data["Revenue (Millions)"] < up_bound)]

more_profitable_films.reset_index()

iqr_rev = more_profitable_films['Revenue (Millions)']
iqr_meta = more_profitable_films['Metascore']
iqr_rating = more_profitable_films['Rating']

#correlation plots

#correlation between  revenue and critic metascore
def metaxrev_correlation():
    meta_rev_corr = sns.regplot(x=iqr_rev, y=iqr_meta, data=data, color='red')
    plt.title('Revenue and Critic Metascore Correlation')
    sns.set_style('darkgrid')
    plt.savefig('metascorexrev_correlation.png', dpi=600, bbox_inches='tight')
    return meta_rev_corr

metaxrev_correlation()


#correlation between revenue and viewer rating
def ratingxrev_correlation():
    rate_rev_corr = sns.regplot(x=iqr_rev, y=iqr_rating, data=data)
    plt.title('Revenue and Viewer Rating Correlation')
    sns.set_style('darkgrid')
    plt.figsize= (6,2)
    plt.savefig('ratingxrev_correlation.png', dpi=600, bbox_inches='tight')
    return rate_rev_corr

ratingxrev_correlation()

np.corrcoef(filtered_rating, filtered_rev)
np.corrcoef(filtered_meta, filtered_rev)

def distribution_plot():
    fig1 = sns.distplot(data['Revenue (Millions)'])
    plt.ylabel('Distribution')
    vals = fig1.get_yticks()
    fig1.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
    sns.set_style('darkgrid')
    plt.figsize= (6,2)
    plt.title('Movie Revenue Distribution')
    plt.savefig('movie_distribution.png', dpi=600, bbox_inches='tight')
    return fig1

distribution_plot()

#genre bar plot
def genre_bar_plot():
    movie_type = data['Genre']
    genres = []
    for index, text in enumerate(movie_type):
        try:
            sep_gens = data['Genre'][index].split(',')
            for item in sep_gens:
                genres.append(item)
        except:
            pass
    unique_genres = list(set(genres))

    tot_gen = []
    for genre in unique_genres:
        tot = genres.count(genre)
        tot_gen.append(tot)
    tot_gen

    genre_dict = dict(zip(unique_genres, tot_gen))

    genre_dict

    popular_genres_chart = sns.barplot(x=unique_genres, y=tot_gen)
    plt.xticks(rotation=90)
    plt.ylabel('Instances')
    plt.title('What Genres Are Most Prevalent Among IMDBs Top Movies?')
    plt.figsize= (6,2)
    plt.savefig('genre_chart.png', dpi=600,bbox_inches='tight')

    return popular_genres_chart

genre_bar_plot()

#data set information
len(data['Revenue (Millions)'])
#there are 64 total null values for metascore
data['Metascore'].isnull().sum()
#there are 0 null values for the rating
data['Rating'].isnull().sum()

#most profitable genre by year

movie_revs = data['Revenue (Millions)']

movie_type = data['Genre']
genres_grouped = []
for index, text in enumerate(movie_type):
    try:
        sep_gens = data['Genre'][index].split(',')
        # print(movie_type)
        genres_grouped.append(sep_gens)
    except:
        pass
#print(genres)
# sep_gens = pd.DataFrame(sep_gens)
# movie_stats = pd.DataFrame(movie_revs + sep_gens)
# movie_stats

pd.DataFrame(genres_grouped)

genres_grouped[1]

#
