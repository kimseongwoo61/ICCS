# -*- coding: utf-8 -*-

import requests
import pandas as pd
import bs4
import time
import os
import copy




# 기능 : base 키워드 파일을 읽고 연관 검색어를 수집하는 함수
# 인자 : base 키워드 파일 경로
# 리턴 값 :
#        - 정상적으로 수집된 연관검색어, base 키워드
#        - 예외가 발생하면 False
def keywordCollector(filedir):
    collectecWord = []

    excel = pd.read_excel(filedir)  # base.xlsx
    keyword_list = excel["Keyword"]  # base.xlsx의 Keyword 시트의 데이터를 모두 읽어드린다.
    site = [
        " site:instagram.com",
        " site:facebook.com",
        " site:youtube.com",
        " site:twitter.com",
        " site:t.me",
        " site:gall.dcinside.com",
        " site:ilbe.com",
        " site:ilbe.com",
        " site:todayhumor.co.kr",
        " site:naver.com",
        " site:daum.net",
        ""
    ]


    index = 0
    for i in keyword_list:
        index += 1

        for j in site:
            # 구글에서 연관 검색어를 xml 형식으로 반환해주는 링크.
            url = "http://suggestqueries.google.com/complete/search?output=toolbar&q=" + str(i) + j

            # xml를 파싱한 뒤 연관 검색어만 추출한다.
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, "lxml")
            tagList = soup.select("suggestion")

            # 추출된 연관 검색어를 collectecWord 리스트에 append 한다.
            for result in tagList:
                collectecWord.append(result['data'])


    # 수짐된 연관 검색어들의 중복된 결과를 제거한다.
    collectecWord = list(set(collectecWord))

    return collectecWord, keyword_list





# 기능 : 연관 검색어를 수집한 뒤 지정된 경로에 결과물을 저장한다.
# 인자 : 연관 검색어를 수집할 base 검색어 저장파일
# 리턴 값 :
#   - 정상적으로 수집 및 저장이 완료되면 True
#   - 문제가 발생하면 False
def RelatedKeyword(filedir, savedir):

    if(os.path.exists(filedir)):
        # 연관검색어 크롤링(수집)을 진행한다.
        keyword, baseKeyword = keywordCollector(filedir)

        # 수집된 키워드를 new_list 경로에 저장한다.
        df = pd.DataFrame(keyword)
        with pd.ExcelWriter(savedir, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Keyword", index=False, header=["Keyword"])
        return True


    else:
        return False




if __name__ == '__main__':
    # 연관 검색어를 추출할 기본(base) 키워드 리스트 파일경로
    base_list  = os.getcwd() + "\\..\\input_data\\base.xlsx"

    # 수집한 연관 검색어를 저장할 파일경로
    new_list   = os.getcwd() + "\\..\\daily_reports\\google.xlsx"
    
    
    print(base_list)
    RelatedKeyword(base_list, new_list)





