import requests
import pandas as pd
import numpy as np
import bs4 as bs

header = {"Accept-Language":"en-US, en;q=0.5"}

url = "https://www.imdb.com/search/title/?groups=top_1000"
results = requests.get(url, header)

soup = bs.BeautifulSoup(results.text, "html.parser")

# The data we need to extract
titles = []
years = []
total_time = []
imdb_ratings = []
meta_scores = []
votes = []
us_gross = []

movie_containers = soup.find_all('div', class_='lister-item mode-advanced')
for containers in movie_containers:

    # extract titles
    title = containers.h3.a.text
    titles.append(title)

    # extract year of release
    year = containers.h3.find('span', class_='lister-item-year text-muted unbold').text
    years.append(year)

    # extract total time of the movie
    if containers.p.find('span', class_='runtime'):
        time = containers.p.find('span', class_='runtime').text
    else:
        time = ''
    total_time.append(time)

    # extract rating given to the movie
    rating = float(containers.strong.text)
    imdb_ratings.append(rating)

    # extract meta_score
    if containers.find('span',class_="metascore favorable"):
        score = containers.find('span',class_="metascore favorable").text
    else:
        score = '0'
    meta_scores.append(score)

    # extract the number of votes and us gross value
    vag = containers.find_all('span', attrs={'name':'nv'})

    # votes
    vote = vag[0].text
    votes.append(vote)

    # gross value in US dollars
    if len(vag) > 1:
        gross = vag[1].text
    else:
        gross = '-'
    us_gross.append(gross)

# Prepare the data extracted in data frame
movies = pd.DataFrame({
    'Movie': titles,
    'Year': years,
    'Total_time(min)': total_time,
    'IMDB ratings': imdb_ratings,
    'Metascore': meta_scores,
    'Votes': votes,
    'US_gross(millions)': us_gross,
})

# Data Cleaning
movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['Votes'] = movies['Votes'].str.replace(',','').astype(int)
movies['Metascore'] = movies['Metascore'].astype(int)
movies['Total_time(min)'] = movies['Total_time(min)'].str.extract('([0-9]+)').astype(int)
print(movies.dtypes)
print(movies['Total_time(min)'].head())














