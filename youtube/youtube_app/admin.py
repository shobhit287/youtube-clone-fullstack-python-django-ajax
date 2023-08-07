from django.contrib import admin
from .models import video_details,watch_later,user_videos_history,like,dislike,user_uploads,comments
admin.site.register(video_details)
admin.site.register(watch_later)
admin.site.register(user_videos_history)
admin.site.register(like)
admin.site.register(dislike)
admin.site.register(user_uploads)
admin.site.register(comments)

# Register your models here.
