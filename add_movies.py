from movie.models import Movie, add_movie

def add():
    f = open('youtube', 'r')
    l = f.read().split('\n')
    while '' in l: l.remove('')
    for line in l:
        data = line.split('\t')
        if len(data) < 3:
            continue
        add_movie('https://www.youtube.com/watch?v='+data[2], data[0])

if __name__ == '__main__':
    add()
