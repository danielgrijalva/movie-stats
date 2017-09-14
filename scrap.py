from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import time

url = 'http://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/released-in-{year}'

def get_html(year):
    '''Get HTML of list of movies of a given year.

    Args:
        year: a year (int).

    Returns:
        html: HTML string.
    '''
    html = requests.get(url.format(year=year)).content
    time.sleep(1)

    return html

def get_gross(html):
    '''Parses HTML data using bs4 to get exact info about movie revenue.

    Args:
        html: text containting HTML webpage.

    Returns:
        gross: list of ints (movie revenue).
    '''
    soup = BeautifulSoup(html, 'html.parser')
    movies = soup.find_all('p', {'class': 'sort-num_votes-visible'})[:10]

    gross = [int(movie.find_all('span')[4]['data-value'].replace(',', '')) for movie in movies]

    return gross

def group_data(year, gross):
    '''Groups year and average gross into a dict.'''
    data = {'year': [year,], 'gross': [gross,]}

    return data


def main():
    '''Generate dataframe with all the data and save it as csv.'''
    data = pd.DataFrame()

    for i in range(1980, 2017):
        gross = np.mean(get_gross(get_html(i)))
        year_gross_dict = group_data(i, gross)

        df = pd.DataFrame.from_dict(year_gross_dict)
        data = pd.concat([data, df])

    data.reset_index(drop=True, inplace=True)
    data.to_csv('data.csv')



if __name__=='__main__':
    main()
