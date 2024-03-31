# Парсинг сайтов

# requests
# BeautifulSoup4
import requests
from bs4 import BeautifulSoup
import json
# Создать функции которые будут работать с базой
import sqlite3





def insert_database(title, content, category_id=1, views=0):
    database = sqlite3.connect('project/db.sqlite3')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO courses_article(title, content, category_id, views) VALUES
    (?,?,?, ?)
    ''', (title, content, category_id, views))
    database.commit()
    database.close()


def select_history():
    database = sqlite3.connect('ls5-61030.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM weather;
    ''')
    history = cursor.fetchall()
    return history

html = requests.get('https://kun.uz/ru').text
soup = BeautifulSoup(html, 'html.parser')

block = soup.find('ul', class_='page-header__menu')
categories = block.find_all('a', class_='menu-link')

json_data = {}
for category in categories:
    category_link = 'https://kun.uz' + category.get('href')
    print(category_link)
    category_title = category.get_text()
    print(category_title)

    json_data[category_title] = []

    html = requests.get(category_link).text
    soup = BeautifulSoup(html, 'html.parser')

    block_news = soup.find('div', {'id': 'news-list'}) # {'class': 'class_name'}
    news = block_news.find_all('div', {'class': 'news'})
    for article in news:
        article_title = article.find('a', class_='news__title').get_text()
        print(article_title)
        try:
            article_description = article.find('div', class_='news__desc').get_text(stript=True)
        except:
            article_description = 'Нет описания'
        print(article_description)
        article_link = 'https://kun.uz' + article.find('a', class_='news__title').get('href')
        print(article_link)
        article_image_link = article.find('img').get('src')
        print(article_image_link)
        article_date = article.find('div', class_='news-meta').get_text()
        print(article_date)
        insert_database(article_title, article_description)


