# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 21:15:21 2023

@author: kimse
"""
import os
import pandas as pd


# 기능 : 수집된 키워드를 total 리스트 파일에 저장하는 함수
# 인자 : 합칠 키워드 수집파일1, 합칠 키워드 수집파일1, base 검색어 리스트
# 리턴 값 :
#        - 정상적으로 키워드를 수집하면 True
#        - 예외가 발생하면 False
def totalMerger(file1, file2, base, savedir):
    total = []

    if os.path.exists(file1) and os.path.exists(file2) and os.path.exists(base):
        excel = pd.read_excel(file1)
        keyword_list1 = excel["Keyword"]
        keyword_list1 = keyword_list1.values.tolist()

        excel = pd.read_excel(file2)
        keyword_list2 = excel["Keyword"]
        keyword_list2 = keyword_list2.values.tolist()

        excel = pd.read_excel(base)
        base_list = excel["Keyword"]
        base_list = base_list.values.tolist()

        total.extend(keyword_list1)
        total.extend(keyword_list2)
        total.extend(base_list)
        total = list(set(total))
        
        df = pd.DataFrame(total)

        with pd.ExcelWriter(savedir, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Keyword", index=False, header=["Keyword"])

    else:
        print("Check your input path!!!")


# 연관 검색어를 추출할 기본(base) 키워드 리스트 파일경로
base_list  = os.getcwd() + "\\..\\input_data\\base.xlsx"

# 수집한 연관 검색어를 저장할 파일경로
new_list1   = os.getcwd() + "\\..\\daily_reports\\naver.xlsx"

new_list2   = os.getcwd() + "\\..\\daily_reports\\google.xlsx"

savedir  = os.getcwd() + "\\..\\daily_reports\\total_keywords.xlsx"

if __name__ == '__main__':
    print(base_list)
    totalMerger(new_list1, new_list2, base_list, savedir)