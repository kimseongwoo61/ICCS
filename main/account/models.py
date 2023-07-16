from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class Token_info(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='token_info')
    
    naver_searchID = models.CharField(max_length=128, unique=True, verbose_name='네이버 검색 client ID')
    naver_searchAPI = models.CharField(max_length=128, unique=True, verbose_name='네이버 검색 API 토큰')
    
    naver_keywordID = models.CharField(max_length=128, unique=True, verbose_name='네이버 검색 client ID')
    naver_keywordAPI = models.CharField(max_length=128, unique=True, verbose_name='네이버 검색 API 토큰')
    
    google_visionID = models.CharField(max_length=128, unique=True, verbose_name='구글 비전 clinet ID')
    google_visionAPI = models.CharField(max_length=128, unique=True, verbose_name='구글 비전 API 토큰')
    
    class Meta:
        db_table = 'token'


