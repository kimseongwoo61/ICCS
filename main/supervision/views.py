from django.shortcuts import render
from django.shortcuts import redirect
from account.models import Token_info
from django.contrib.auth.models import User
from .src import illegalContents
from .src import search_google as Google
from .src import search_naver as Naver
from .src import htmlProcessing
from django.contrib.sessions.backends.db import SessionStore
from .src import gen_report
import shutil
import pandas as pd
import os

base_dir = os.path.abspath('.').replace('\\','/') + "/supervision/src/"
reports_template = base_dir + "유해 콘텐츠 단속 보고서.xlsx"


def session_set(request, flag, value):
    # 세션 객체 생성 또는 가져오기
    session = SessionStore(session_key=request.session.session_key)

    # 세션에 플래그 설정
    session[flag] = value
    session.save()
    
def session_url_checker(request, flag, value):
    # 세션 객체 생성 또는 가져오기
    session = SessionStore(session_key=request.session.session_key)

    # 세션검증
    if flag in session:
        
        if session[flag] == value:
            return True
        
        else:
            return False
        
    else:
        return False

def extact_keywords(text):
    keywords = []
    trimed_text = text.lstrip().rstrip()
    
    if(trimed_text == ";" or trimed_text == ""):
        return False
    
    for index in text.split(';'):
        if index == "":
            continue
        keywords.append(index.lstrip().rstrip())
    
    return keywords

def move_files(source_folder, destination_folder):
    # 소스 폴더 내부의 모든 파일 목록 얻기
    file_list = os.listdir(source_folder)

    # 파일을 목적지 폴더로 이동
    for file_name in file_list:
        # 파일의 전체 경로 생성
        source_file = os.path.join(source_folder, file_name).replace("\\", "/")
        destination_file = os.path.join(destination_folder, file_name).replace("\\", "/")

        # 파일 이동
        shutil.move(source_file, destination_file)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'supervision/dashboard.html')

def monitor(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'supervision/monitor.html')
    


def check_urls(request):
    # 요약정보를 전달하기 위한 리스트와 유저 input를 저장한다.
    result = []
    url = request.POST.get('URL')
    
    
    # 만약 클라이언트가 전달한 데이터가 정확한 URL 형식이 맞는지 검증한다.
    if(illegalContents.validate_url(url) == False):
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"정확한 URL 형식으로 입력해 주세요."})
   
    
    #try:
    user_reports_xlsx = base_dir + "user/" + request.user.username + "/result/유해 콘텐츠 단속 보고서.xlsx"
    user_url_illegal_image = base_dir + "user/" + request.user.username + "/check"
    user_reports_image = base_dir + "user/" + request.user.username + "/result/image"
    
    
    print("check_urls --------- start")
    
    # url 유해성 검사 결과를 받아 온다.
    # 페이지 제목, 도메인, 블랙리스트 키워드 여부, 유해 이미지 정보, 유해성 평가 점수, 콘텐츠 요약정보
    title, url, \
    domain, \
    check_blackList, \
    image_dirInfo, \
    score_illegal, \
    summary = illegalContents.checker(request, url, 0)
    
    
    # 리포트 생성을 위한 템플릿 파일을 유저 작업 공간으로 복사한다.
    shutil.copyfile(reports_template, user_reports_xlsx)
    
    # 추출된 유해 이미지를 유저 리포트 작성 공간으로 복사한다.
    move_files(user_url_illegal_image, user_reports_image)
    gen_report.save_data(user_reports_xlsx, 
                         title, 
                         url, 
                         domain, 
                         check_blackList, 
                         summary, 
                         image_dirInfo, 
                         score_illegal)
    
    
    # 웹 페이지 결과 출력을 위한 요약 정보를 저장 후 웹 페이지에 출력한다.
    result.append(title)
    result.append(url)
    result.append(domain)
    result.append(check_blackList)
    result.append(len(image_dirInfo))
    
    # 웹 컨텐츠 요약정보를 200자 이하로 유지한다.
    if(len(summary) > 200):
        result.append(summary[0:200])
    
    else:
        result.append(summary)
    
    
    print("check_urls --------- finish")
    return render(request, 'supervision/results.html', 
                  {'url':True, 'reports':result})
    
    
    #except Exception as e:
    #    print("check_urls --------- error : " + str(e))
    #    return render(request, 'supervision/results.html', 
    #                  {'url':False, 'reports':"서버 내부 에러가 발생하였습니다. 잠시 후 다시 시도해 주세요."})
    
    

def check_keywords(request):
    
    # 로그인 여부를 먼저 확인한다.
    if not request.user.is_authenticated:
        return redirect('/')
    
    
    if(os.path.exists(base_dir + "/user/" + request.user.username)):
        try:
            shutil.rmtree(base_dir + "/user/" + request.user.username)
            os.mkdir(base_dir + "/user/" + request.user.username)
            os.mkdir(base_dir + "/user/" + request.user.username + "/check")
            os.mkdir(base_dir + "/user/" + request.user.username + "/result")
            os.mkdir(base_dir + "/user/" + request.user.username + "/result/image")
        
        except Exception as e:
            print("illegalContents checker --------- Error " + str(e))
    
    else:
        os.mkdir(base_dir + "/user/" + request.user.username)
    
    
    # 유저 input을 저장한 뒤, 검색 데이터를 수집하기 위한 키워드를 파싱한다.
    user_input = request.POST.get('keywords')
    search_engine = request.POST.get('submit')
    keywords = extact_keywords(user_input)
    search_result = base_dir + "/user/" + request.user.username + "/"
    user_reports_xlsx = base_dir + "user/" + request.user.username + "/result/유해 콘텐츠 단속 보고서.xlsx"
    user_url_illegal_image = base_dir + "user/" + request.user.username + "/check"
    user_reports_image = base_dir + "user/" + request.user.username + "/result/image"
    
    print("check_keywords --------- start")
    
    # 정상적인 검색 키워드 입력 형식이 아니라면,
    # 재입력을 유도한다.
    if keywords == False:
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"정확한 키워드 형식으로 입력해 주세요."})
    
    # 리포트 생성을 위한 템플릿 파일을 유저 작업 공간으로 복사한다.
    shutil.copyfile(reports_template, user_reports_xlsx)
    
    try:
        # User 모델과 One-to-One 관계인 Token_info 모델
        user = User.objects.get(username=request.user.username)
        
        # 역참조를 통해 Token_info 객체에 접근
        token_info = user.token_info  
        
        # naver 검색 API를 통해 데이터를 수집, 문서화 한다.
        if search_engine == "naver":
            for query in keywords:
                title, link, displayLink = Naver.search_naver(query, token_info.naver_searchID, 
                                                              token_info.naver_searchAPI, 100)
                
                Naver.gen_xlsx(title, displayLink, link, search_result + "naver.xlsx")
            
    
        # google 검색 API를 통해 데이터를 수집, 문서화 한다.
        elif search_engine == "google":
            for query in keywords:
                title, displayLink, link = Google.search_google(query, token_info.google_searchID, 
                                                                token_info.google_searchAPI, 1)
                Google.gen_xlsx(title, displayLink, link, search_result + "google.xlsx")
        
            
            df = pd.read_excel(search_result + "google.xlsx")
            link = df['url'].tolist()
            
            print("검색결과를 모두 수집하였습니다.")
            for urls in link:
                print("검증진행 - " + str(urls))
                title, url, \
                domain, \
                check_blackList, \
                image_dirInfo, \
                score_illegal, \
                summary = illegalContents.checker(request, urls, 1)
                
                move_files(user_url_illegal_image, user_reports_image)
                gen_report.save_data(user_reports_xlsx, 
                                     title, 
                                     url, 
                                     domain, 
                                     check_blackList, 
                                     summary, 
                                     image_dirInfo, 
                                     score_illegal)
        
            
        
        # google, naver가 아닌 요청은 비정상 요청으로 간주한다.
        else:
            return render(request, 'supervision/results.html', 
                          {'url':False, 'reports':"비정상적인 요청입니다."})
        
        
        
        
        
    
        # 작업이 완료되면 알림을 전달한다.
        print("check_keywords --------- finish")
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"작업이 완료되었습니다."})
    
    
    # 서버 내부 에러에 따른 예외처리
    except Exception as e:
        print("check_keywords --------- error : " + str(e))
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"서버 내부 에러가 발생하였습니다. 잠시 후 다시 시도해 주세요."})
        
        
    


    
    

    