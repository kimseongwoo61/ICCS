# 파일 다운로드, 업로드를 위해 사용
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse

# 페이지 리다이렉션, 렌더링, User 토큰 정보 로딩
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# 유해정보 검사를 위해 별도로 제작한 검사 코드
from .src import illegalContents
from .src import search_google as Google
from .src import search_naver as Naver
from .src import gen_report
from .src import data_encrypt

# 관리자에 대한 문의 정보를 처리하기 위해 모델정보를 import 한다.
from account.models import QnA
import datetime

# 페이지 강제 리다이렉션을 진행목적으로 사용
from django.shortcuts import redirect

# 문의글 개수 구분을 위해서 사용함
from django.core.paginator import Paginator

# 파이썬 기본 라이브러리
import shutil
import pandas as pd
import os
import threading
lock = threading.Lock()

# 동작 로깅용도
import logging
logger = logging.getLogger('django')

# 파일 처리에 사용되는 경로는 가능한 모두 절대경로를 사용하도록 한다.
base_dir = os.path.join(os.path.abspath('.'), "supervision", "src")
reports_template = os.path.join(base_dir, "유해 콘텐츠 단속 보고서.xlsx")


import re

def validate_phone_number(phone_number):
    # 정규표현식을 사용하여 XXX-XXXX-XXXX 형식의 전화번호를 검사합니다.
    pattern = r'^\d{3}-\d{4}-\d{4}$'
    
    if re.match(pattern, phone_number):
        return True
    else:
        return False


# 검색결과를 수집할 검색어를 받은다음 올바른 형식인지 검사하고, 검색어를 리스트로 반환한다.
# input : 사용자 입력값(검색어1;검색어;...)
# return : 올바른 형식이면 리스트 반환([검색어1, 검색어2, ...])
def extact_keywords(text):
    keywords = []
    
    # 입력 값의 좌우 불필요 공백을 제거한다.
    trimed_text = text.strip()
    
    # 단순 세미콜론이거나 값이 없으면 False를 반환한다.
    if(trimed_text == ";" or trimed_text == ""):
        return False
    
    # ;기준으로 키워드를 분리한다.
    for index in text.split(';'):
        temp_keyword = index.strip()
        
        # ;;;... 이런 형식의 데이터는 삭제한다.
        if temp_keyword == "":
            continue
        
        keywords.append(temp_keyword)
    
    return keywords


# 폴더를 통째로 다른 경로에 옮기기 위한 코드
# input : 복사하려는 파일경로, 이동하고 싶은 경로
# return : 작업 성공 유무(bool)
def move_files(source_folder, destination_folder):
    
    if not os.path.exists(source_folder):
        return False
    
    # 소스 폴더 내부의 모든 파일 목록 얻기
    file_list = os.listdir(source_folder)

    # 파일을 목적지 폴더로 이동
    for file_name in file_list:
        # 파일의 전체 경로 생성
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)

        # 파일 이동
        shutil.move(source_file, destination_file)
    
    return True


# 대시보드 페이지 랜더링
@login_required(login_url='/')
def dashboard(request):    
    return render(request, 'supervision/dashboard.html')

# 단속진행 지원 페이지 렌더링
@login_required(login_url='/')
def monitor(request):    
    return render(request, 'supervision/monitor.html')

# Q&A 작성 페이지
@login_required(login_url='/')
def write(request):    
    return render(request, 'supervision/write.html')


# 관리자 Q&A 리스트 조회 페이지 -> 관리자만 접근 가능
@login_required(login_url='/')
def qna(request):
    
    # 접근 계정의 정보가 admin이 아니면 홈 디렉터리로 강제 리다이렉션한다.
    if request.user.is_superuser == False:
        return redirect("/")
    
    # 문의글 작성시간 기준으로 정렬한 전체 데이터를 가져온다
    qna_information = QnA.objects.all().order_by("date")
    
    # 문의 글을 한 페이지당 5개씩 끊어서 출력하도록 한다.
    page = int(request.GET.get('p', 1)) #없으면 1로 지정
    paginator = Paginator(qna_information, 5) #한 페이지 당 몇개 씩 보여줄 지 지정 
    boards = paginator.get_page(page)
    return render(request, "supervision/qna.html", {"boards":boards, "total_boards_count": boards.paginator.count})



# 게시글 전체 정보 처리 페이지
@login_required(login_url='/')
def check_qna(request):
    logger.info("[*] check_urls - START")
        
    # 관리자는 문의 사항을 확인하는 기능만 가지고 있다.
    if request.user.is_superuser == False:
        try:
            # 사용자로부터 제목과 문의내용을 입력받는다.
            # XSS와 같은 특수문자 공격은 템플릿 단에서 모두 이스케이프 처리한다.
            
            # 작성자 아이디, 제목, 내용, 작성시간 정보를 QnA 모델에 저장한다.
            user_id = request.user.username
            title = request.POST.get("title").strip()
            contents = request.POST.get("contents").strip()
            name = request.POST.get("Name").strip()
            number = request.POST.get("number").strip()
            
            # 만약 제목이나 내용이 공백이면 다시 작성하도록 함.
            if title == "" or contents == "" or validate_phone_number(number) == False:
                return render(request, 'supervision/write.html', {"result" : "올바르지 않은 형식"})
            
        
            now = datetime.datetime.now()
            write_time = now.strftime('%Y-%m-%d')
            
            qna = QnA(user_id = user_id, title = title, contents = contents, date = write_time, name = name, phone_number = number )
            qna.save()
            
            return render(request, 'supervision/write.html', {"result" : True})
        
        # 만약 에러가 발생하면 실패여부를 출력한다.
        except Exception as e:
            logger.info("[*] check_urls - ERROR : " + str(e))
            return render(request, 'supervision/write.html', {"result" : False})
    
    # 관리자가 접근하면 홈 디렉터리로 리다이렉트한다.
    else:
        return redirect("/")
            

# 단일 URL의 콘텐츠 유해성을 검사 및 결과를 렌더링
@login_required(login_url='/')
def check_urls(request):
    logger.info("[*] check_urls - START")
    
    # 요약정보를 전달하기 위한 리스트와 유저 input를 저장한다.
    result = []
    url = request.POST.get('URL')
    
    
    # 유저가 입력한 URL이 정확한 데이터가 맞는지 정규식 검증을 진행한다.
    if(illegalContents.validate_url(url) == False):
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"정확한 URL 형식으로 입력해 주세요."})
        
    
    try:
        # 요청 작업이 수행중임을 알 수 있도록 임계영역 설정
        lock.acquire()
        
        # 작업 결과 엑셀 리포트 저장경로
        user_reports_xlsx = os.path.join(base_dir, "user", request.user.username, "result", "유해 콘텐츠 단속 보고서.xlsx")
        
        # 작업 결과 엑셀 리포트에 사용될 이미지 경로
        user_reports_image = os.path.join(base_dir, "user", request.user.username, "result", "image")
        
        # URL에 존재하는 이미지 임시 저장경로
        user_url_illegal_image = os.path.join(base_dir, "user", request.user.username, "check")
        
        
        # url 유해성 검사 결과를 받아 온다.
        
        # URL에서 추출한 이미지 구분번호 용도의 인덱스
        index = 0
        
        # 페이지 제목, 도메인, 블랙리스트 키워드 여부, 유해 이미지 정보, 유해성 평가 점수, 콘텐츠 요약정보
        title, url, \
        domain, \
        check_blackList, \
        image_dirInfo, \
        score_illegal, \
        summary, \
        whois_information = illegalContents.checker(request, url, 0, index)
        
        
        # 리포트 생성을 위한 템플릿 파일을 유저 작업 공간으로 복사한다.
        shutil.copyfile(reports_template, user_reports_xlsx)
        
        # 추출된 유해 이미지를 유저 리포트 작성 공간으로 복사한다.
        move_files(user_url_illegal_image, user_reports_image)
        
        # URL 유해성 검사 결과를 기반으로 엑셀 리포트 제작을 진행한다.
        username = request.user.username
        
        gen_report.save_data(user_reports_xlsx, 
                             title, 
                             url, 
                             domain, 
                             check_blackList, 
                             summary, 
                             image_dirInfo, 
                             score_illegal, 
                             username)
        
        
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
        
        # 작업이 정상적으로 완료 되었으므로 락 해제
        lock.release()
        logger.info("[*] check_urls - FINISH")
        
        # 처리 결과를 유저에게 알리도록 렌더링 진행
        return render(request, 'supervision/results.html', 
                      {'url':True, 'reports':result, 'whois':whois_information})
    
    
    # 가끔 가다가 API 서버측의 통신 불안정으로 검사로직이 작동하지 않거나,
    # 유저의 네트워크 문제가 존재하는 경우, 유저에게 에러경고를 띄운다.
    except Exception as e:
        
        # 작업이 비정상적으로 완료 되었어도 락 해제
        lock.release()
        logger.warning("[!] check_urls - ERROR : " + str(e))
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"서버 내부 에러가 발생하였습니다. 잠시 후 다시 시도해 주세요."})
    
    
# 키워드 기반 검색결과 유해성 검증 및 결과 렌더링
@login_required(login_url='/')
def check_keywords(request):
    logger.info("[*] check_keywords - START")
    
    # 요청 작업이 수행중임을 알 수 있도록 임계영역 설정
    lock.acquire()

    
    # 이전 작업 정보들은 모두 삭제 후, 작업 결과를 저장할 폴더를 생성함.
    user_directory = os.path.join(base_dir, "user", request.user.username)
    
    if(os.path.exists(user_directory)):
        try:
            shutil.rmtree(user_directory)
            os.mkdir(user_directory)
            os.mkdir(os.path.join(user_directory, "check"))
            os.mkdir(os.path.join(user_directory, "result"))
            os.mkdir(os.path.join(user_directory, "result", "image"))
        
        # 만일 위 과정에서 에러가 발생해도 문제 없으므로 그냥 서버측 로깅 후 다음 코드 진행
        except Exception as e:
            logger.warning("[!] check_keywords - ERROR : " + str(e))
    
    else:
        os.mkdir(user_directory)
    
    
    # 유저 input을 저장한 뒤, 검색 데이터를 수집하기 위한 키워드를 파싱한다.
    user_input = request.POST.get('keywords')
    search_engine = request.POST.get('submit')
    keywords = extact_keywords(user_input)
    
    # 검색결과 추출 및 콘텐츠 저장, 검증, 결과물 저장을 위한 경로를 지정한다.
    user_reports_xlsx = os.path.join(user_directory, "result", "유해 콘텐츠 단속 보고서.xlsx")
    user_url_illegal_image = os.path.join(user_directory, "check")
    user_reports_image = os.path.join(user_directory, "result", "image")

    # 정상적인 검색 키워드 입력 형식이 아니라면 재입력을 유도한다.
    if keywords == False:
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"정확한 키워드 형식으로 입력해 주세요."})
    
    # 리포트 템플릿 파일을 유저 작업 공간으로 복사한다.
    shutil.copyfile(reports_template, user_reports_xlsx)
    
    
    try:
        # User 모델과 One-to-One 관계인 Token_info 모델
        user = User.objects.get(username=request.user.username)
        
        # 역참조를 통해 Token_info 객체에 접근
        token_info = user.token_info  
        
        # 회원가입 시 생성한 개인키 생성 경로를 설정
        user_name = request.user.username
        aes_key_dir = os.path.join(os.path.abspath('.'), "user_key", user_name, "aes.key")
        
        
        # naver 검색 API를 통해 데이터를 수집, 문서화 한다.
        if search_engine == "naver":
            
            # 검색 API 사용을 위한 토큰, ID 정보를 복호화 한다.
            naver_searchID = data_encrypt.decrypt_aes(token_info.naver_searchID, aes_key_dir)
            naver_searchAPI = data_encrypt.decrypt_aes(token_info.naver_searchAPI, aes_key_dir)
            
            # 검색결과가 엑셀로 저장되는 경로
            search_result_dir = os.path.join(user_directory, "naver.xlsx")
            
            for query in keywords:
                
                # 검색어 기반, 검색결과를 수집한다.
                title, link, displayLink = Naver.search_naver(query, naver_searchID, naver_searchAPI, 10)
                
                # 검색결과를 엑셀파일로 저장한다.
                Naver.gen_xlsx(title, displayLink, link, search_result_dir)
            df = pd.read_excel(search_result_dir)
            link = df['url'].tolist()
            logger.info("[?] 검색결과 수집 완료")
    
    
        # google 검색 API를 통해 데이터를 수집, 문서화 한다.
        elif search_engine == "google":
            
            # 검색 API 사용을 위한 토큰, ID 정보를 복호화 한다.
            google_searchID = data_encrypt.decrypt_aes(token_info.google_searchID, aes_key_dir)
            google_searchAPI = data_encrypt.decrypt_aes(token_info.google_searchAPI, aes_key_dir)
            
            # 검색결과가 엑셀로 저장되는 경로
            search_result_dir = os.path.join(user_directory, "google.xlsx")
            
            for query in keywords:
                
                # 검색어 기반, 검색결과를 수집한다.
                title, displayLink, link = Google.search_google(query, google_searchID, google_searchAPI, 10)
                
                # 검색결과를 엑셀파일로 저장한다.
                Google.gen_xlsx(title, displayLink, link, search_result_dir)
            df = pd.read_excel(search_result_dir)
            link = df['url'].tolist()
            logger.info("[?] 검색결과 수집 완료")
        
        
        # google, naver가 아닌 요청은 비정상 요청으로 간주한다.
        else:
            # 작업이 비정상적으로 완료 되었어도 락 해제
            lock.release()
            return render(request, 'supervision/results.html', 
                          {'url':False, 'reports':"비정상적인 요청입니다."})
        
        
        # 검색 결과에서 추출된 URL 리스트에서 중복제거를 진행한다.
        link = list(set(link))
        
        # URL별 수집된 이미지의 구분번호 인덱스
        index = 0
        for urls in link:
            logger.info("URL 유해성 검증진행 : " + str(urls))

            title, url, \
            domain, \
            check_blackList, \
            image_dirInfo, \
            score_illegal, \
            summary, \
            whois_reports = illegalContents.checker(request, urls, 1, index)
            
            index += 1
            
            username = request.user.username
            move_files(user_url_illegal_image, user_reports_image)
            gen_report.save_data(user_reports_xlsx, 
                                 title, 
                                 url, 
                                 domain, 
                                 check_blackList, 
                                 summary, 
                                 image_dirInfo, 
                                 score_illegal,
                                 username)
    
        # 작업이 정상적으로 완료 되었으므로 락 해제
        lock.release()
        logger.info("[*] check_keywords - FINISH")
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"작업이 완료되었습니다. 리포트를 확인해 주세요.", 'search_engine':True})

    # 서버 내부 에러에 따른 예외처리
    except Exception as e:
        lock.release()
        logger.warning("[!] check_keywords - ERROR : " + str(e))
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"서버 내부 에러가 발생하였습니다. 잠시 후 다시 시도해 주세요."})
   
     
# 제작된 리포트를 다운로드할 수 있는 페이지 렌더링 진행
@login_required(login_url='/')
def export_reports(request):
    logger.info("[*] check_keywords - START")
    
    # 리포트 파일이 저장될 경로를 설정한다.
    username = request.user.username
    reports_dir = os.path.join(base_dir, "user", username, "result")
    
    
    if os.path.exists(reports_dir):
        os.chdir(os.path.join(reports_dir, ".."))
        shutil.make_archive("reports", "zip", "./result")
        
        # 원래 작업 디렉터리로 복귀한다.
        os.chdir(os.path.join(reports_dir, "..", "..", "..", "..", ".."))        
        fs = FileSystemStorage(os.path.join(reports_dir, ".."))
        response = FileResponse(fs.open(os.path.join(reports_dir, "..", "reports.zip"), 'rb'))
        response['Content-Disposition'] = 'attachment; filename=reports.zip'
        return response
    
    else:
        return render(request, 'supervision/results.html', 
                      {'url':False, 'reports':"생성된 리포트 정보가 없습니다."})
    


    
    

    