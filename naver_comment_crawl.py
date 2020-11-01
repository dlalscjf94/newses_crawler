"""""""""""""""""""""""
네이버 특정 기사 댓글 크롤링
"""""""""""""""""""""""

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
from datetime import datetime


# 댓글 크롤링을 원하는 url 입력
def get_url():

    url = ''

    while 'news.naver.com/main/' not in str(url):
        # url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=032&aid=0003040669'
        # 네이버뉴스가 아닐경우 댓글 크롤링 불가
        url = input("댓글 수집을 원하시는 url을 입력해주세요 : ")

        # 최종 url
        # 네이버 뉴스 댓글 불러오기 + '&m_view=1' '&sort=LIKE' => 추가하면 좋아요 순
        # https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=277&aid=0004783392&m_view=1

        url = url + '&m_view=1'

        # 댓글주소
        # print(url)

    # 최종 url을 return
    return url


def crawl_comment(url):

    # 댓글 리스트
    comment_lst = []

    # 제목 리스트
    title_lst = []

    # 지정된 시간동안 안되면 종료 하는 코드
    # driver.implicitly_wait()

    # 드라이버 생성
    driver = webdriver.Chrome()

    # 해당 주소 열기
    driver.get(url)

    time.sleep(4)

    title = driver.find_element_by_id("articleTitle")

    print("========================================")

    print("기사제목 : ", title.text)

    print("========================================")

    try:

        while True:
            driver.find_element_by_class_name("u_cbox_btn_more").click()

            time.sleep(1.5)

    # 더이상 안보이면 이제 그만하고 pass
    except exceptions.ElementNotVisibleException as e:

        print("마지막 댓글에 도달했습니다. ")

        pass

    # 다른 예외 발생시 확인
    except Exception as e:

        print("마지막 댓글에 도달했습니다. ")

        pass

    html = driver.page_source
    # xml로 받아내고
    dom = BeautifulSoup(html, "lxml")

    # 댓글이 들어있는 페이지 전체 댓글 갖고오기
    comments = dom.find_all("span", {"class" : "u_cbox_contents"})

    # 댓글이 하나도 없다면:
    if len(comments) == 0:

        print("해당 기사의 댓글이 없습니다.")

    else:
        # 댓글의 text만 뽑아내기
        for comment in comments:

            # print(str(comment.text))
            comment_lst.append(str(comment.text))
            title_lst.append(title.text)

    return comment_lst, title_lst


#  댓글모음 xlsx 파일 생성
def make_xlsx(comment_lst, title_lst):

    dict = {"댓글내용": comment_lst, "기사제목" : title_lst}

    df = pd.DataFrame(dict)

    # 뉴스기사제목이 엑셀파일명에 들어가도록 설정
    df.to_excel("단일기사 댓글" + ".xlsx", sheet_name='sheet1')

    return


def main():

    url = get_url()

    comment_lst, title_lst = crawl_comment(url)

    make_xlsx(comment_lst, title_lst)

    print("해당 기사의 댓글 수집이 완료되었습니다.")


if __name__ == '__main__':

    main()
