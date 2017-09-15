import pandas as pd
import requests
import time

url = 'http://www.boxofficemojo.com/yearly/chart/?yr={year}'

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
    data = pd.read_html(html, match='Rank')
    box_office = data[0][3][6:50]
    theaters = data[0][4][6:50]

    return box_office, theaters


def format_numbers(dataframe):
    '''Remove '$' and ',' from each row.'''
    dataframe = dataframe.replace('[\$,]', '', regex=True).astype(int)

    return dataframe

def group_data(year, avg_gross, theaters):
    '''Groups year and average gross into a dict.'''
    data = {'year': [year,], 'gross': [avg_gross,], 'theaters': [theaters,]}

    return data


def main():

    data = pd.DataFrame()

    for i in range(1980, 2017):
        gross, theaters = read_html(get_html(i))
        gross = int(format_numbers(gross).mean())
        theaters.fillna(inplace=True, value=0)
        theaters = int(format_numbers(theaters).mean())
        year_gross_dict = group_data(i, gross, theaters)

        df = pd.DataFrame.from_dict(year_gross_dict)
        data = pd.concat([data, df])

    data.reset_index(drop=True, inplace=True)
    data.to_csv('data.csv', index=False)


if __name__=='__main__':
    main()
