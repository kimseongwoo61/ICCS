<<<<<<< HEAD
# Generated by Django 4.2.2 on 2023-06-29 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=32, unique=True, verbose_name='사용자 아이디')),
                ('user_pw', models.CharField(max_length=128, verbose_name='사용자 패스워드')),
                ('user_name', models.CharField(max_length=16, unique=True, verbose_name='사용자 이름')),
                ('user_email', models.CharField(max_length=128, unique=True, verbose_name='사용자 이메일')),
                ('user_register', models.DateTimeField(auto_now=True, verbose_name='계정 생성시간')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
=======
# Generated by Django 4.2.2 on 2023-06-29 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=32, unique=True, verbose_name='사용자 아이디')),
                ('user_pw', models.CharField(max_length=128, verbose_name='사용자 패스워드')),
                ('user_name', models.CharField(max_length=16, unique=True, verbose_name='사용자 이름')),
                ('user_email', models.CharField(max_length=128, unique=True, verbose_name='사용자 이메일')),
                ('user_register', models.DateTimeField(auto_now=True, verbose_name='계정 생성시간')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
>>>>>>> 719cd225de0c04018c059ed171d0c81cd36fa789
