# Generated by Django 4.2.2 on 2023-08-17 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_qna'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qna',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
