# Generated by Django 4.2.3 on 2023-08-07 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_app', '0022_remove_user_videos_history_user_videos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_videos_history',
            name='user_videos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='youtube_app.user_uploads'),
        ),
        migrations.AlterField(
            model_name='user_videos_history',
            name='videos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='youtube_app.video_details'),
        ),
    ]
