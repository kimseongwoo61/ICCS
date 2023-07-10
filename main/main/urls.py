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
    
    # 관리자 접속 페이지
    path('admin/', admin.site.urls),
    
    #----------------------------------------------
    # 최초 접속시 로그인 또는 회원가입 페이지
    path('', ac.login),
    
    # 회원가입 페이지
    path('join/', ac.join),
    
    # 회원정보 확인을 위한 페이지
    path('check/', ac.check, name='check'),
    
    #----------------------------------------------
    # 최초 단속 관리 대시보드
    path('dashboard/', sp.dashboard),
    
    # 단속 설정 및 시행 페이지
    #path('supervision/', sp.index),
]
