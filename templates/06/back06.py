# 03-116: Web Scrapper

from flask import render_template
import requests
from bs4 import BeautifulSoup
import datetime
import re

def naiz_titularrak_orain():
    url = 'https://www.naiz.eus'
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        print(f'ERROR: Can\'t render {url}, {response.status_code}!')
        return render_template('404/index_404.html')

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    titularrak = []

    date_scrapper = re.compile(r'/(\d{4})(\d{2})(\d{2})/')

    for article in articles:
        title_tag = article.find('h3', class_='article__title')
        link_tag = title_tag.find('a') if title_tag else None
        author_tag = article.find('a', class_='article__author')
        image_tag = article.find('img')

        title = title_tag.get_text(strip=True) if title_tag else "Sin título"
        link = link_tag['href'] if link_tag else "#"
        author = author_tag.get_text(strip=True) if author_tag else "Desconocido"
        image = image_tag['src'] if image_tag else "https://via.placeholder.com/300"

        # Convertir URL relativa en absoluta
        if link.startswith("/"):
            link = url + link
            
        if image.startswith("/"):
            image = url + image

        
        # Date reformatter
        date_found = date_scrapper.search(link)

        if date_found:

            year, month, day = date_found.groups()
            date = f'{year}-{month}-{day}'

        else:

            datetime.datetime.now().strftime("%Y-%m-%d")


        titularrak.append({
            'title': title,
            'link': link,
            'author': author,
            'image': image,
            'date':  date
        })

    return titularrak


print(naiz_titularrak_orain())
