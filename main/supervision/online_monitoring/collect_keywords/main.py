

import os
import threading

import naver
import googles
import merger_xlsx
# 연관 검색어를 추출할 기본(base) 키워드 리스트 파일경로
base_list  = os.getcwd() + "\\..\\input_data\\base.xlsx"

# 수집한 연관 검색어를 저장할 파일경로
google_list   = os.getcwd() + "\\..\\daily_reports\\google.xlsx"
naver_list   = os.getcwd() + "\\..\\daily_reports\\naver.xlsx"

# 최종 연관검색어 정보가 저장될 파일경로
total_list  = os.getcwd() + "\\..\\daily_reports\\total_keywords.xlsx"

# 구글, 네이버 검색엔진을 통해 각각의 연관검색어 정보를 수집한다.
t1 = threading.Thread(target=googles.RelatedKeyword, args=(base_list, google_list))
t2 = threading.Thread(target=naver.collect, args=(base_list, naver_list))
t1.start()
t2.start()

t1.join()
t2.join()
print("done")

merger_xlsx.totalMerger(google_list, naver_list, base_list, total_list)