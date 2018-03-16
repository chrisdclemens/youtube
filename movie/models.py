from django.db import models
import random
from .get_soup import get_soup

# Create your models here.
class Movie(models.Model):
    url = models.CharField(max_length=200)
    imdb = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    length = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    genres = models.CharField(max_length=200) # this will be a comma-delimited list of genre IDs
    keywords = models.CharField(max_length=200) # comma-delimited list of keywords
    image = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Genre(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default='')
    def __str__(self): return self.title

class Keyword(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self): return self.title

def add_movie(url, inp_imdb):
    print(url)
    if inp_imdb[:4] == 'http':
        imdb = inp_imdb.split('/')[4]
    else:
        imdb = inp_imdb
    print(imdb)
    try:
        movie = Movie.objects.get(imdb=imdb)
        return
    except:
        pass
    m = Movie(url=url)
    m.imdb = imdb
    info = get_movie_info(imdb)
    m.title = info['title']
    m.length = info['length']
    m.year = info['year']
    m.genres = ','.join([str(genre_id(g)) for g in info['genres']])
    m.keywords = ','.join([str(keyword_id(k)) for k in info['keywords']])
    m.image = info['image']
    m.save()

def genre_id(inp_name):
    name = inp_name.strip()
    try:
        genre = Genre.objects.get(title=name)
    except:
        genre = Genre.objects.create(title=name)
    return genre.id

def keyword_id(inp_name):
    name = inp_name.strip()
    try:
        keyword = Keyword.objects.get(title=name)
    except:
        keyword = Keyword.objects.create(title=name)
    return keyword.id

def get_movie_info(imdb):
    page_url = 'http://www.imdb.com/title/'+imdb
    page_soup = get_soup(page_url)
    title = page_soup.find('h1', {'itemprop': 'name'}).text.split('\xa0')[0]
    year = page_soup.find('h1', {'itemprop': 'name'}).text.split('\xa0')[1][1:-2]
    if len(year) != 4:
        year = input('year: ')
    try:
        length = page_soup.find('time').attrs['datetime'][2:-1]
    except:
        length = input('length: ')
    genre_links = page_soup.find('div', {'itemprop': 'genre'}).findAll('a')

    genres = [a.text for a in genre_links]

    try:
        post = page_soup.find('div', {'class': 'poster'})
        img = post.find('img').attrs['src']
    except:
        img = 'https://i.media-imdb.com/images/mobile/film-40x54.png'

    keywords_url = page_url + '/keywords'
    page_soup = get_soup(keywords_url)
    keyword_sodas = page_soup.findAll('div', {'class': 'sodatext'})
    keywords = [k.text[1:-1] for k in keyword_sodas]

    return {'imdb': imdb,
            'title': title,
            'length': int(length),
            'year': int(year),
            'genres': genres,
            'keywords': keywords,
            'image': img,
            }

def filter_movie_number(filter_object_query):
    filter_object = dict(filter_object_query.lists())
    movie_objects = []
    for m in Movie.objects.all():
        if pass_filter(filter_object, m):
            movie_objects.append(m)
            if len(movie_objects) > 99:
                break
    return len(movie_objects)

def get_random_movie(filter_object_query):
    filter_object = dict(filter_object_query.lists())
    movies = []
    for m in Movie.objects.all():
        if pass_filter(filter_object, m):
            movies.append(m.id)
    return random.choice(movies)

def pass_filter(filter_object, m):
    if int(m.year) < int(filter_object['min_year'][0]): return False
    if int(m.year) > int(filter_object['max_year'][0]): return False
    if int(m.length) < int(filter_object['min_runtime'][0]): return False
    if int(m.length) > int(filter_object['max_runtime'][0]): return False
    if 'genres_exclude[]' in filter_object.keys():
        for g in m.genres.split(','):
            if g in filter_object['genres_exclude[]']:
                return False
    if 'genres_include[]' in filter_object.keys():
        for g in filter_object['genres_include[]']:
            if g not in m.genres.split(','):
                return False
    return True

def youtube_link_lives(youtube):
    page_soup = get_soup(youtube)
    if page_soup.find('title').text == 'YouTube':
        return False
    return True
