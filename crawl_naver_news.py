
"""""""""""""""""""""""""""""""""""""""""""""
네이버 뉴스크롤링 코드입니다. + 댓글 크롤링 기능 추가
"""""""""""""""""""""""""""""""""""""""""""""


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


# 키워드 입력받아 넘겨주는 함수
def get_keyword():

    # 키워드 날짜 받아서 넘겨주기, 정확하게 입력해서 확정할때까지 입력
    while True:

        keyword = input("키워드를 입력하세요 : ")

        st_date = input("해당 키워드에 대한 수집 시작잉을 입력해주세요 (YYYYMMDD) : ")

        ed_date = input("해당 키워드에 대한 수집 종료일을 입력해주세요 (YYYYMMDD) : ")

        # 시작일 00시 00분 부터 종료일 00시 00분까지 내용 검색
        s_date = st_date[0:4] + '.' + st_date[4:6] + '.' + st_date[6:8] + '.00.00'
        e_date = ed_date[0:4] + '.' + ed_date[4:6] + '.' + ed_date[6:8] + '.00.00'

        # print(s_date)
        # print(e_date)

        print("=================================================================")
        print("키워드 : ", keyword)
        print("시작일 : ", s_date)
        print("종료일 : ", e_date)
        print("=================================================================")

        x = input("입력한 키워드, 날짜를 확인하세요. (확정 => 1 입력, 재입력 -> 2 입력) : ")

        if x == '1':

            return keyword, s_date, e_date

        else:

            get_keyword()

# 키워드와 기간 이용하여 뉴스 검색 및 링크 리스트 생성
def crawl_naver_news(keyword, s_date, e_date):

    # 네이버 뉴스를 담을 라스트 선언
    link_lst = []

    # 에러코드 세팅
    errcode = 0

    # url 구성정보 확인, keyword => 검색어
    # url => https://search.naver.com/search.naver?where=news&sm=tab_jum&query='keyword'

    # 최신순, 1일 지정하고 해당 키워드에 대해 1일치 조사
    # https://search.naver.com/search.naver?&where=news&query=%EB%82%A0%EC%94%A8&sm=tab_pge&sort=1&photo=0&field=0
    # &reporter_article=&pd=4&ds=2020.10.30.17.11&de=2020.10.31.17.11&docid=&nso=so:dd,p:1d,a:all&mynews=0&start=1&refresh_start=0

    # start 부분 +10씩 증가시켜서 마지막페이지까지 도달하기

    # start 세팅
    i = 1

    # 에러코드가 0보다 작아지면 종료
    while errcode >= 0:

        url = 'https://search.naver.com/search.naver?&where=news&query={}&sm=tab_pge&sort=1&photo=0&field=0&' \
              'reporter_article=&pd=4&ds={}&de={}&docid=&nso=so:dd,p:1d,a:all&mynews=0&start={}&refresh_start=0'\
            .format(keyword, s_date, e_date, i)

        # 드라이버 세팅
        driver = webdriver.Chrome()

        print(url)

        driver.get(url)

        try:

            check = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/p")

            print(check.text)

            # 검색결과가 없는 페이지까지 도달하면
            if "검색결과가 없습니다" in check.text:

                # errcode = -1 반환
                errcode = -1

            else:

                print("크롤링을 다시 진행하세요")

                return 0

        except:

            time.sleep(5)

            # news_list 내 url 꺼내기 (naver가 들어있는 경우만)

            a_tags = driver.find_elements_by_tag_name('a')

            for a_tag in a_tags:

                link = a_tag.get_attribute('href')

                # 네이버뉴스에 속하는 뉴스일 경우 리스트에 링크를 추가
                if 'news.naver.com/main/' in str(link):

                    link_lst.append(link)

                else:

                    pass

            print(link_lst)

            driver.close()

            i = i + 10

    return link_lst


# 뉴스 본문과 제목을 크롤링
def crawl_link(link_lst):

    # 뉴스 제목들을 담을 리스트 선언
    title_lst = []

    # 뉴스 본문을 담을 리스트 선언
    content_lst = []

    # 기사입력 시간
    news_regi_time_lst = []

    # 언론사 => 이미지 타이틀로 언론사 이름 갖고오기
    press_lst = []

    for i in range(0, len(link_lst), 1):

        driver = webdriver.Chrome()

        driver.get(link_lst[i])

        time.sleep(3)

        # 제목 끌어내기
        title = driver.find_element_by_id('articleTitle')

        print("========================================================")

        print("뉴스 제목 :  ", title.text)

        title_lst.append(title.text)

        print("========================================================")

        # 본문 끌어내기
        content = driver.find_element_by_id('articleBodyContents')

        print("뉴스 본문")

        print("========================================================")

        print(content.text)

        content_lst.append(content.text)

        # content_text = content.text.replace('\n', '')

        # content_lst.append(content_text)

        print("========================================================")

        # 언론사 > img > title
        a = driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td[1]/div/div[1]/div[1]/a/img")
        press = a.get_attribute('title')
        press_lst.append(press)

        # 뉴스등록시간 : t11
        b = driver.find_element_by_class_name('t11')
        reg_time = b.text
        news_regi_time_lst.append(reg_time)

        driver.close()

        time.sleep(3)

    return link_lst, title_lst, content_lst, press_lst, news_regi_time_lst


# 각 뉴스에서 댓글을 크롤링
def crawl_comment(link_lst, title_lst, press_lst):

    # 댓글 리스트
    comment_lst = []

    # 기사 제목 리스트
    comment_title_lst = []

    # 기사 url 리스트
    comment_link_lst = []

    # 해당 댓글 기사 언론사 리스트
    comment_press_lst = []

    driver = webdriver.Chrome()

    # 댓글창 죽소 = url + &m_view=1 '&sort=LIKE' => 추가하면 좋아요 순

    # 지정된 시간동안 안되면 종료
    # driver.implicitly_wait

    for i in range(0, len(link_lst), 1):

        url = link_lst[i] + '&m_view=1'

        driver.get(url)

        time.sleep(5)

        try:

            while True:
                driver.find_element_by_class_name("u_cbox_btn_more").click()

                time.sleep(1.5)

        # 더이상 안보이면 이제 그만하고 pass
        except exceptions.ElementNotVisibleException as e:

            print("최종 댓글에 도달했습니다.")

            pass

        # 다른 예외 발생시 확인
        except Exception as e:

            print(e)

            pass

        html = driver.page_source
        # xml로 받아내고
        dom = BeautifulSoup(html, "lxml")

        # 댓글이 들어있는 페이지 전체 댓글 갖고오기
        comments = dom.find_all("span", {"class": "u_cbox_contents"})

        for comment in comments:

            comment_lst.append(str(comment.text))
            comment_title_lst.append(title_lst[i])
            comment_link_lst.append(link_lst[i])
            comment_press_lst.append(press_lst[i])

        # comment_lst = comment_lst + comments

    return comment_lst, comment_title_lst, comment_link_lst, comment_press_lst


# 결과물을 xlsx 파일로 출력
# 파일 제목이 네이버뉴스 + 기간 +_키워드가 되도록 설정 추가
def make_xlsx(link_lst, title_lst, content_lst, press_lst, news_regi_time_lst, s_date, e_date, keyword):

    # 엑셀파일 생성을 위한 딕셔너리 생성
    dict = {"뉴스 제목": title_lst, "뉴스 본문": content_lst, "뉴스 링크": link_lst, "언론사": press_lst, "등록시간": news_regi_time_lst}

    df = pd.DataFrame(dict)

    # print(df)

    xlsx_title = '네이버뉴스' + '(' + s_date + ') ~ (' + e_date + ')' + keyword

    df.to_excel(xlsx_title + '.xlsx', sheet_name='sheet1')

    return


# 댓글모음 엑셀파일 생성
def make_comments_xlsx(comment_lst, comment_title_lst, comment_link_lst, comment_press_lst,  keyword, s_date, e_date):

    # 댓글모음 dict 생성
    dict = {"댓글": comment_lst, "기사제목": comment_title_lst, "URL": comment_link_lst, "언론사": comment_press_lst}

    df = pd.DataFrame(dict)

    # 엑셀파일명 설정
    xlsx_title = '네이버_댓글' + '(' + s_date + ') ~ (' + e_date + ')' + keyword

    # DataFrame 엑셀파일로 생성
    df.to_excel(xlsx_title + '.xlsx', sheet_name='sheet1')


    return


def main():

    keyword, s_date, e_date = get_keyword()

    link_lst = crawl_naver_news(keyword, s_date, e_date)

    link_lst, title_lst, content_lst, press_lst, news_regi_time_lst = crawl_link(link_lst)

    make_xlsx(link_lst, title_lst, content_lst, press_lst, news_regi_time_lst, s_date, e_date, keyword)

    comment_lst, comment_title_lst, comment_link_lst, comment_press_lst = crawl_comment(link_lst, title_lst, press_lst)

    make_comments_xlsx(comment_lst, comment_title_lst, comment_link_lst, comment_press_lst,  keyword, s_date, e_date)


if __name__ == '__main__':

    main()

    print("작업이 완료되었습니다.")



