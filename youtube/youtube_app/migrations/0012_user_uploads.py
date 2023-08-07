# Generated by Django 4.2.3 on 2023-08-03 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_app', '0011_like_dislike'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_uploads',
            fields=[
                ('video_id', models.AutoField(primary_key=True, serialize=False)),
                ('video_title', models.CharField(max_length=150)),
                ('video_category', models.CharField(max_length=100)),
                ('video_description', models.TextField(default='')),
                ('video_thumbnail', models.ImageField(upload_to='thumbnail')),
                ('video_timestamp', models.DateTimeField()),
                ('video_duration', models.CharField(default='', max_length=20)),
                ('video_views', models.IntegerField(default=0)),
                ('video_videofile', models.FileField(upload_to='upload')),
            ],
        ),
    ]