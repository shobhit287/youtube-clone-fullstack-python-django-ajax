# Generated by Django 4.2.3 on 2023-08-03 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_app', '0014_user_uploads_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_uploads',
            name='video_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]