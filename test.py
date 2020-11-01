"""
네이버 기사 댓글 추출
"""


# 데이터 엑셀 저장 및 dataFrame 운용을 위한 pandas import
import pandas as pd

# 크롤링한 텍스트 정규화를 위한 re import
import re

# 기본 크롤링을 위한 webdriver import
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# selenium exception
from selenium.common import exceptions

url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=032&aid=0003040669'

driver = webdriver.Chrome()

# 댓글창 죽소 = url + &m_view=1 '&sort=LIKE' => 추가하면 좋아요 순

# 지정된 시간동안 안되면 종료
# driver.implicitly_wait

url = url + '&m_view=1'

driver.get(url)

time.sleep(5)

try:

    while True:

        driver.find_element_by_class_name("u_cbox_btn_more").click()

        time.sleep(1.5)

# 더이상 안보이면 이제 그만하고 pass
except exceptions.ElementNotVisibleException as e:

    print(e)

    pass

# 다른 예외 발생시 확인
except Exception as e:

    print(e)

    pass

html = driver.page_source
# xml로 받아내고
dom = BeautifulSoup(html, "lxml")

# 댓글이 들어있는 페이지 전체 댓글 갖고오기
comments = dom.find_all("span", {"class" : "u_cbox_contents"})

# 댓글의 text만 뽑아내기
for comment in comments:

    print(comment.text)
