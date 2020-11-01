"""""""""""""""""""""
구글 뉴스크롤링 코드입니다.
"""""""""""""""""""""

# 데이터 엑셀 저장 및 dataFrame 운용을 위한 pandas import
import pandas as pd

# html 크롤링을 위한 Beautifulsoup
from bs4 import BeautifulSoup

# 기본 크롤링을 위한 webdriver import
from selenium import webdriver
import time

# selenium exception
from selenium.common import exceptions

# 크롤링한 텍스트 정규화를 위한 re import
import re

import requests
from bs4 import BeautifulSoup
import urllib


def main():

    keyword_input = "파이썬"
    keyword = urllib.parse.quote(keyword_input)
    print("파이썬 문자열을 URL로 변환: ", keyword)

    base_url = "https://news.google.com"
    search_url = base_url + "/search?q=" + keyword + "&hl=ko&gl=KR&cied=KR%3Ako"
    print("검색어와 조합한 URL: ", search_url)

    def google_news_clipping_keyword(keyword_input, limit=5):
        keyword = urllib.parse.quote(keyword_input)
        url = base_url + "/search?q=" + keyword + "&hl=ko&gl=KR&cied=KR%3Ako"

        resp = requests.get(url)
        html_src = resp.text
        soup = BeautifulSoup(html_src, "html.parser")

        news_items = soup.select('div[class="xrnccd"]')

        links = []
        titles = []
        contents = []
        agencies = []
        reporting_dates = []
        reporting_times = []

        for item in news_items[:limit]:
            link = item.find('a', attrs={'class': 'VDXfz'}).get('href')
            news_link = base_url + link[1:]
            links.append(news_link)

            news_title = item.find('a', attrs={'class': "DY5T1d"}).get('href')
            titles.append(news_title)

            news_content = item.find('span', attrs={'class': 'xBbh9'}).text
            contents.append(news_content)

            news_agency = item.find('a', attrs={'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).text
            agencies.append(news_agency)

            news_reporting = item.find('time', attrs={'class': 'WW6dff uQIVzc Sksgp'})
            news_reporting_datetime = news_reporting.get('datetime').split("T")
            news_reporting_date = news_reporting_datetime[0]
            news_reporting_time = news_reporting_datetime[1][:-1]
            reporting_dates.append(news_reporting_date)
            reporting_times.append(news_reporting_time)

        result = {'link': links, 'title': titles, 'contents': contents, 'agency': agencies, \
                  'date': reporting_dates, 'time': reporting_times}

        return result

    search_word = input('검색어를 입력하세요: ')
    news = google_news_clipping_keyword(search_word, 2)
    print(news['link'])
    print(news['agency'])
    return


if __name__ == '__main__':
    main()