import requests
import logging
import datetime

import pandas as pd

from bs4 import BeautifulSoup
from mysql.connector import MySQLConnection, Error

def scrape_official_webtoons(host, port, user, password, database):
    # set today's date
    today = datetime.date.today()

    URL = 'https://www.webtoons.com/id/genre'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="card_wrap genre")

    webtoons = {'title': [],
                'author': [],
                'likes': [],
                'url':[],
                'genre':[],
                'subscribers':[],
                'star_score':[],
                'unsuitable_for_children':[],
                'date':[],
                'title_id':[]
                }

    genre_elements = results.find_all("ul", class_="card_lst")
    for g in genre_elements:

        webtoon_elements = g.find_all("a")
        for w in webtoon_elements:
            webtoon_title = w.find("p", class_="subj").text
            webtoon_author = w.find("p", class_="author").text
            webtoon_likes = w.find("em", class_="grade_num").text

            webtoon_a_html = str(w).split('>')[0]+'/>'
            webtoon_a_soup = BeautifulSoup(webtoon_a_html, "html.parser")
            webtoon_url = webtoon_a_soup.find('a').get('href')
            webtoon_unsuitable_for_children = webtoon_a_soup.find('a').get('data-title-unsuitable-for-children')

            webtoon_title_page = requests.get(webtoon_url)
            webtoon_title_soup = BeautifulSoup(webtoon_title_page.content, "html.parser")

            webtoon_genre = webtoon_title_soup.find("h2", class_="genre").text
            webtoon_subscribers = webtoon_title_soup.find("em", class_="cnt").text
            webtoon_star_score = webtoon_title_soup.find("em", class_="cnt", id="_starScoreAverage").text


            # convert numeric values
            webtoon_likes = webtoon_likes.replace(".","")
            webtoon_likes = webtoon_likes.replace(",",".")
            if 'RB' in webtoon_likes:
                webtoon_likes = int(float(webtoon_likes.replace("RB",""))*1000)
            elif 'JT' in webtoon_likes:
                webtoon_likes = int(float(webtoon_likes.replace('JT',''))*1000000)
            else:
                webtoon_likes = int(float(webtoon_likes))

            webtoon_subscribers = webtoon_subscribers.replace(".","")
            webtoon_subscribers = webtoon_subscribers.replace(",",".")
            if 'RB' in webtoon_subscribers:
                webtoon_subscribers = int(float(webtoon_subscribers.replace("RB",""))*1000)
            elif 'JT' in webtoon_subscribers:
                webtoon_subscribers = int(float(webtoon_subscribers.replace('JT',''))*1000000)
            else:
                webtoon_subscribers = int(float(webtoon_subscribers))

            webtoon_star_score = float(webtoon_star_score.replace(',','.'))

            # Update dictionary
            webtoons['title'].append(webtoon_title)
            webtoons['author'].append(webtoon_author)
            webtoons['likes'].append(webtoon_likes)
            webtoons['unsuitable_for_children'].append(webtoon_unsuitable_for_children)
            webtoons['genre'].append(webtoon_genre)
            webtoons['url'].append(webtoon_url)
            webtoons['subscribers'].append(webtoon_subscribers)
            webtoons['star_score'].append(webtoon_star_score)
            webtoons['date'].append(today)
            webtoons['title_id'].append(webtoon_url.split('=')[-1])
    
    df = pd.DataFrame.from_dict(webtoons)
    logging.info(df)
    logging.info(df.info())

    conn = MySQLConnection(host=host, port=port, user=user, password=password, database=database)
    df.to_sql(con=conn, name='webtoon_officials', flavor='mysql', if_exists='append', index=False)
    conn.close()

if __name__ == '__main__':
    scrape_official_webtoons()