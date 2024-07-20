# Generated by Django 4.2.2 on 2023-08-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_token_info_google_visionapi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token_info',
            name='google_searchAPI',
            field=models.BinaryField(default=b'', unique=True, verbose_name='구글 검색 API 토큰'),
        ),
        migrations.AlterField(
            model_name='token_info',
            name='google_searchID',
            field=models.BinaryField(default=b'', unique=True, verbose_name='구글 검색 client ID'),
        ),
        migrations.AlterField(
            model_name='token_info',
            name='google_visionAPI',
            field=models.BinaryField(default=b'', unique=True, verbose_name='구글 비전 API 토큰 암호정보'),
        ),
        migrations.AlterField(
            model_name='token_info',
            name='google_visionID',
            field=models.BinaryField(default=b'', unique=True, verbose_name='구글 비전 clinet ID'),
        ),
        migrations.AlterField(
            model_name='token_info',
            name='naver_searchAPI',
            field=models.BinaryField(default=b'', unique=True, verbose_name='네이버 검색 API 토큰'),
        ),
        migrations.AlterField(
            model_name='token_info',
            name='naver_searchID',
            field=models.BinaryField(default=b'', unique=True, verbose_name='네이버 검색 client ID'),
        ),
    ]