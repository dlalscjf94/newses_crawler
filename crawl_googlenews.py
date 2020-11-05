from newsapi import NewsApiClient
import requests
import json
import pandas as pd


# 모든 소스를 불러와서 language ='en', country = 'us' 인 경우만 살려내기
# All articles mentioning Apple from yesterday, sorted by popular publishers first
# https://newsapi.org/v2/everything?q=apple&from=2020-11-02&to=2020-11-02&sortBy=popularity&apiKey=API_KEY


# set api
# 발금받은 api 값
def set_api():
    # Init
    # 발급받은 api_key 값 입력
    newsapi = NewsApiClient(api_key='abe284ff60df4ce3a1bb407a1c3b2a1b')

    return newsapi


# set_url
# url에 들어갈 검색어, 기간을 입력, url 세팅 및 return
# 유명 언론사부터 나오도록 : sortBy=popularity
def get_sources(newsapi):

    # base_url = 'https://newsapi.org/v2/everything?q={}&from={}&to={}&sortBy=popularity&apiKey={}'

    # 검색 키워드 설정
    q = input("검색활 키워드를 입력해주세요 : ")

    # 본문에 제외할 키워드 설정
    exc_keyword = input("제외할 키워드를 입력해주세요 : ")

    # 시작일 설정
    st_date = input("시작일을 입력해주세요(YYYYMMDD) : ")

    # 변환
    s_date = st_date[0:4] + '-' + st_date[4:6] + '-' + st_date[6:8]

    # 종료일 설정
    ed_date = input("종료일을 입력해주세요(YYYYMMDD) : ")

    # 변환
    e_date = ed_date[0:4] + '-' + ed_date[4:6] + '-' + ed_date[6:8]

    # pageSize => 100 고정
    pagesize = 100

    # 최대 검색 결과값 100 이므로 페이지 1 고정 (2페이지부터 불러지지 않음)
    page = 1

    # 유명한 순으로 적용 &sortBy=popularity
    sources = newsapi.get_everything(q=q, from_param=s_date, to=e_date, page_size=pagesize, page=page,
                                     sort_by='popularity')

    print(sources)

    # 엑셀 파일명 미리 생성
    xlsx_title = '구글뉴스' + '(' + st_date + ')' + '~' + '(' + ed_date + ')' + '_' + q

    return sources, exc_keyword, xlsx_title

"""
추출한 기사들 조작하는 코드
def manu_sources(sources):

    data = json.dumps(sources)

    print(data)

    dict = json.loads(data)

    print(json.dumps(dict, indent = 4, sort_keys=True))

    return dict

"""


def manu_sources(sources, exc_keyword):

    name_lst = []
    author_lst = []
    content_lst = []
    desc_lst = []
    publish_lst = []

    # key, value
    # key 확인
    print("=================================================")

    for key in sources.keys():

        print(key, ":", sources[key])

        print("=================================================")

    print("수신 상태 확인 : ", sources["status"])
    print("총 기사 건수 : ", sources["totalResults"])
    print("=============================================================")

    # arricles 키의 값인 기사들을 가져오기
    json_lst = sources.get('articles')

    for obj in json_lst:

        # 본문이 존재하지 않으면 pass
        if obj['content'] == None:

            pass

        # 제외할 키워드가 본문내에 존재한다면 pass
        elif exc_keyword in obj['content']:

            pass

        else:

            print("신문사 : ", obj['source'].get('name'))
            name_lst.append(obj['source'].get('name'))

            print("작성자 : ", obj['author'])
            author_lst.append(obj['author'])

            print("본문 : ", obj['content'])
            content_lst.append(obj['content'])

            print("요약 : ", obj['description'])
            desc_lst.append(obj['description'])

            print("작성일자 : ", obj['publishedAt'])
            publish_lst.append(obj['publishedAt'])

        print("=============================================================")

    return name_lst, author_lst, content_lst, desc_lst, publish_lst


# 결과물을 엑셀파일로 만들어주는 함수
def make_xlsx(name_lst, author_lst, content_lst, desc_lst, publish_lst, xlsx_title):

    dict = {"언론사": name_lst, "작성자": author_lst, "본문": content_lst, "요약": desc_lst, "작성일자": publish_lst}

    df = pd.DataFrame(dict)

    df.to_excel(xlsx_title + ".xlsx", sheet_name='sheet1')

    return


def main():

    # api 요청하는것을 tot_page 만큼 반복시키면 될듯, 한번에 호출할 수 있는 기사의 수 : 100
    newsapi = set_api()

    # 뉴스 기사
    sources, exc_keyword, xlsx_title = get_sources(newsapi)

    name_lst, author_lst, content_lst, desc_lst, publish_lst = manu_sources(sources, exc_keyword)

    make_xlsx(name_lst, author_lst, content_lst, desc_lst, publish_lst, xlsx_title)

    print("작업이 완료되었습니다.")


if __name__ == '__main__':

    main()









