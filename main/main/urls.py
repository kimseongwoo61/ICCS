"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from account import views as ac
from supervision import views as sp

urlpatterns = [
    
    # ----------------------------------------------
    # 관리자 접속 페이지
    path('admin/', admin.site.urls),
    
    
    # ----------------------------------------------
    # 최초 접속시 로그인 또는 회원가입 페이지
    path('', ac.login_first),
    
    # 회원가입 페이지
    path('join/', ac.join),
    
    # 내 정보 조회 페이지
    path('myinfo/', ac.myinfo),
    
    # 내 정보 수정 요청 데이터 검증 및 반영을 위한 페이지
    path('check_info/', ac.change_myinfo, name='check'),
    
    # 로그인 입력 정보 확인을 위한 페이지
    path('check/', ac.check, name='check'),
    
    # 로그아웃 처리를 위한 페이지
    path('logout/', ac.logout, name='logout'),
    
    
    # ----------------------------------------------
    # 최초 단속 관리 대시보드
    path('dashboard/', sp.dashboard),
    
    # 단속시행 페이지
    path('monitor/', sp.monitor),

    
    # 관리자 문의 페이지
    path('write/', sp.write),
    
    # 관리자 문의 조회 페이지
    path('qna/', sp.qna),
    
    # 게시글 전체 정보 처리 페이지
    path('check_qna/', sp.check_qna),
    
    
    
    # ----------------------------------------------
    # 단일 URL 점검 페이지
    path('check_urls/', sp.check_urls),
    
    # 다중 검색키워드 검증 페이지
    path('check_keywords/', sp.check_keywords),
    
    
    # ----------------------------------------------
    # 리포트 및 결과물을 다운로드하기 위한 페이지
    path('download_reports/', sp.export_reports)
    
]
