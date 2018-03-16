from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Movie, Genre, add_movie, filter_movie_number, get_movie_info, youtube_link_lives, get_random_movie
from .populate import populate_from_reddit, populate_from_youtube_playlist
import random

def index(request):
    return HttpResponse("hello world")

def watch(request, movie_id):
    m = Movie.objects.get(id=movie_id)
    template = loader.get_template('movie/watch.html')
    yt_id = m.url.split('=')[-1]
    context = {'yt_id': yt_id}
    return HttpResponse(template.render(context, request))

def add(request):
#    populate_from_reddit('exploitation', 50)
    add_by_hand()
#    populate_from_youtube_playlist('PLu4YvG4BytjMLQPIgJHsTiiFxuju6gkf_')

def add_by_hand():
    current_num = len(Movie.objects.all())
    print('Currently there are %s movies.' % str(current_num))
    num = int(input('How many to add? '))
    while len(Movie.objects.all()) < current_num + num:
        add_movie(input('URL: '), input('IMDB: '))

def purge(request):
    i = len(Movie.objects.all())
    for m in Movie.objects.all():
        i -= 1
        print(i)
        if not youtube_link_lives(m.url):
            m.delete()

def choose(request):
    template = loader.get_template('movie/choose.html')

    context = {}
    context['init_number'] = len(Movie.objects.all())
    context['genres'] = Genre.objects.all()
    context['min_year'] = min([m.year for m in Movie.objects.all()])
    context['max_year'] = max([m.year for m in Movie.objects.all()])
    context['min_runtime'] = min([m.length for m in Movie.objects.all()])
    context['max_runtime'] = max([m.length for m in Movie.objects.all()])

    return HttpResponse(template.render(context, request))

def filter(request):
    data = request.GET
    movies = filter_movie_number(data)
    return JsonResponse({'movies': movies})

def random_movie(request):
    data = request.GET
    rand = get_random_movie(data)
    return JsonResponse({'choice': rand})

