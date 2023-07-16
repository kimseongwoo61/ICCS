from django.shortcuts import render
from django.shortcuts import redirect
from account.models import Token_info
from .src import illegalContents
from django.contrib.sessions.backends.db import SessionStore



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


# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'supervision/dashboard.html')


def monitor(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'supervision/monitor.html')
    

def check_urls(request):
    # 먼저 중복요청 여부를 확인한다.
    
    # 이미 검증을 요청한 상황인가?
    #if session_url_checker(request, 'url_checker', True):
    #    return render(request, 'supervision/monitor.html', {'url':True, 'reports':"이미 검증 작업을 요청하였습니다. \n잠시만 기다려주세요."})
        
    
    
    result = []
    url = request.POST.get('URL')
    #session_set(request, 'url_checker', True)
    
    
    #if illegalContents.validate_url(url) == False:
    #    return
    

    score, imageInfo, check, summary = illegalContents.checker(request, url)
    result.append(score)
    result.append(imageInfo)
    result.append(check)
    result.append(summary)
    
    #session_set(request, 'url_checker', False)
    return render(request, 'supervision/monitor.html', {'url':True, 'reports':result, 'user':request.user.username})
    

def check_keywords(request):
    print("asdf")
    
    

    