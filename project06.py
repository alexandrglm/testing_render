############################################################################
# Project 06: Basic content scrapper using requests, bs4 and so on.
################
# Imports: 
from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime
###############
# app.route to Blueprint rooute:
project06 = Blueprint('project06', __name__)
###############
# 06 Main
@project06.route('/') 
def render_project_06():

    articles = naiz_titularrak_orain()
    return render_template('06/index_06.html', articles=articles)

def naiz_titularrak_orain():

    url = 'https://www.naiz.eus'
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        print(f"ERROR: Get {response.status_code} error loading {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    titularrak = []

    for article in articles:

        title_tag = article.find('h3', class_='article__title')
        link_tag = title_tag.find('a') if title_tag else None
        author_tag = article.find('a', class_='article__author')
        image_tag = article.find('img')

        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        link = link_tag['href'] if link_tag else "#"
        author = author_tag.get_text(strip=True) if author_tag else "Unknown"
        image = image_tag['src'] if image_tag else "https://picsum.photos/300/300"

        if link.startswith("/"):
            link = url + link
        if image.startswith("/"):
            image = url + image

        titularrak.append({

            'title': title,
            'link': link,
            'author': author,
            'image': image,
            'date': datetime.now().strftime("%Y-%m-%d")
        })

    return titularrak