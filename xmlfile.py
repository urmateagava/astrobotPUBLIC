from bs4 import BeautifulSoup as bs
import requests




def astro(sign:str, day:str):
    url = 'https://thebesturlever'
    page = requests.get(url)
    soup = bs(page.text, 'lxml')
    fst = soup.find(f'{sign}')
    sec = fst.find(f'{day}').text
    return sec

