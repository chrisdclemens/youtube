from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def get_soup(url):
    page = uReq(url)
    html = page.read()
    page_soup = soup(html, 'html.parser')
    return page_soup
