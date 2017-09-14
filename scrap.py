import pandas as pd
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

    return html


def read_html(html):
    '''Using pandas.read_html() to extract table inside HTML string.

    Args:
        html: HTML string returned from get_html()

    Returns:
        box_office: DataFrame object containing revenue info of 50 movies.
    '''
    data = pd.read_html(html)[1]
    box_office = data[['Domestic Box Office']][:50]

    return box_office


def format_currency(dataframe):
    '''Remove '$' and ',' from each row.'''
    dataframe = dataframe.replace('[\$,]', '', regex=True).astype(int)
    return dataframe

def group_data(year, avg_gross):
    '''Groups year and average gross into a dict.'''
    data = {'year': [year,], 'gross': [avg_gross,]}

    return data


def main():

    data = pd.DataFrame()

    for i in range(1980, 2017):
        gross = int(format_currency((read_html(get_html(i)))).mean())
        year_gross_dict = group_data(i, gross)

        df = pd.DataFrame.from_dict(year_gross_dict)
        data = pd.concat([data, df])

    data.reset_index(drop=True, inplace=True)
    data.to_csv('data.csv')


if __name__=='__main__':
    main()
