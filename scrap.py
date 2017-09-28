import requests
from bs4 import BeautifulSoup
import time
import re

url = ('http://www.imdb.com/search/title?count=100&view=simple'
    '&boxoffice_gross_us=1,&title_type=feature&release_date={year}')

headers = {'Accept-Language': 'en-US'}


def get_movies(year):
    '''Get list of movies released in <year>.'''
    movies_html = requests.get(url.format(year=year), headers=headers).content
    soup = BeautifulSoup(movies_html, 'html.parser')
    movies = soup.findAll('a', {'href': re.compile('adv_li_i$')})

    return ['http://www.imdb.com' + m['href'] for m in movies]

def go_to_movie(url):
    '''Get IMDb page of a movie.'''
    movie_html = requests.get(url, headers=headers).content

    return movie_html

def scrap_titlebar(soup):
    '''Get name, rating, genre, year, release date and score of a movie.'''
    name = soup.find('h1', {'itemprop': 'name'}).text.strip()[:-7]
    genre = soup.find('span', {'itemprop': 'genre'}).text
    score = float(soup.find('span', {'itemprop': 'ratingValue'}).text)
    released = soup.find('meta', {'itemprop': 'datePublished'})['content']
    year = soup.find('span', {'id': 'titleYear'}).find('a').text
    try:
        rating = soup.find('meta', {'itemprop': 'contentRating'})['content']
    except TypeError:
        rating = 'Not Rated'

    return {'name': name, 'rating': rating, 'genre': genre, 'year': year, 'released': released, 'score': score}

def scrap_summary(soup):
    '''Get director, writer and star of a movie.'''
    director = soup.find('span', {'itemprop': 'director'}).find('span').text
    writer = soup.find('span', {'itemprop': 'creator'}).find('span').text
    star = soup.find('span', {'itemprop': 'actors'}).find('span').text

    return {'director': director, 'writer': writer, 'star': star}

def scrap_details(soup):
    '''Get country, budget, gross, production co. and runtime of a movie.'''
    country = soup.find('a', {'href': re.compile('country')}).text
    gross = soup.find('h4', string='Gross:').parent.contents[2].strip()
    company = soup.find('a', {'href': re.compile('company'), 'itemprop': 'url'}).find('span').text
    try:
        budget = soup.find('h4', string='Budget:').parent.contents[2].strip()
    except AttributeError:
        budget = 0
    try:
        runtime = int(soup.find_all('time', {'itemprop': 'duration'})[1].text[:-3])
    except IndexError:
        runtime = 100

    gross = float(gross.replace('$','').replace(',',''))
    budget = float(budget.replace('$','').replace(',',''))

    return {'country': country, 'budget': budget, 'gross': gross, 'company': company, 'runtime': runtime}

def main():
    for year in range(1986, 2017):
        movies = get_movies(year)

        for movie_url in movies:
            movie = go_to_movie(movie_url)
            soup = BeautifulSoup(movie, 'html.parser')
            titlebar = scrap_titlebar(soup)
            summary = scrap_summary(soup)
            details = scrap_details(soup)
            print(details)
            time.sleep(1)

if __name__ == '__main__':
    main()
