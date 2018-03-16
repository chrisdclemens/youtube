import praw, json
from .models import Movie, add_movie, youtube_link_lives, get_soup
from .get_soup import get_soup

def get_reddit_object():
    reddit = praw.Reddit(client_id='PKR0QLfOQGO2kw', client_secret='k_ttn7gjIy3m14LPKSAy60TMeFg', user_agent='ringerforaringer')
    return reddit

def populate_from_reddit(subreddit, num_to_get):
    movies = []
    visited = []
    reddit = get_reddit_object()
    subreddit = reddit.subreddit(subreddit)
    while len(movies) < num_to_get:
        submission = subreddit.random()
        if submission.url in visited:
            continue
        visited.append(submission.url)
        if youtube_in_db(submission.url):
            continue
        if not youtube_link_lives(submission.url):
            continue
        url = submission.url.split('&')[0]
        print(submission.title)
        print(submission.id)
        imdb = input('IMDb: ')
        if imdb == '': continue
        movies.append((url, imdb))
    print('Adding movies')
    i = len(movies)
    for m in movies:
        i -= 1
        print(i)
        add_movie(m[0], m[1])

def youtube_in_db(youtube):
    print(youtube)
    if 'https://www.youtube.com/watch?v=' not in youtube: return True
    try:
        m = Movie.objects.get(url=youtube)
        return True
    except:
        return False

def get_json(url):
    page_soup = get_soup(url)
    return json.loads(page_soup.text)

def populate_from_youtube_playlist(playlist_id):
    youtube_urls = []
    apikey = 'AIzaSyDwDD321hnPvOlFOUoqWe1J_lVv3g8cKPw'
    url_template = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId=%s&key=%s' % (playlist_id, apikey)
    url = url_template
    data = get_json(url)
    total_results = data['pageInfo']['totalResults']
    results_per_page = data['pageInfo']['resultsPerPage']
    for i in range(int(total_results / results_per_page)+1):
        print(i)
        data = get_json(url)
        youtube_urls += [item['contentDetails']['videoId'] for item in data['items']]
        next_page = data['nextPageToken']
        url = url_template + '&pageToken='+next_page
        f = open('youtube ids', 'w')
        f.write('\n'.join(youtube_urls))
        f.close()

def get_youtube_urls(html):
    urls = []
    for line in html.split('\n'):
        if 'videoId' in line:
            urls.append(line.split('"')[3])
    return urls

