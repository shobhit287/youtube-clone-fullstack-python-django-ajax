from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('youtube/video/<int:id>', views.videoplayback,name="playback"),
    path('youtube/category/<str:slug>', views.category,name="category"),
    path('youtube/search-suggestion', views.search_suggestions,name="search-suggestions"),
    path('youtube/search/<param>', views.search,name="search"),
    path('youtube/signup', views.handlesignup,name="signup"),
    path('youtube/logout', views.handlelogout,name="logout"),
    path('youtube/login', views.handlelogin,name="signin"),
    path('youtube/watchlater/<int:id>', views.watchlater,name="watchlater"),
    path('youtube/watchlater-list', views.show_watch_later,name="watchlater"),
    path('youtube/watchlater/remove/<int:id>', views.remove_watch_video,name="remove_watchlater"),
    path('youtube/history', views.history_show,name="history_show"),
    path('youtube/history/remove/<param>', views.history_remove,name="history_remove"),
    path('youtube/history/remove/1abc745bf-g', views.history_remove,name="history_remove"),
    path('youtube/like/<int:id>', views.like_update,name="like"),
    path('youtube/dislike/<int:id>', views.dislike_update,name="dislike"),
    path('youtube/user-upload', views.user_upload,name="userupload"),
    path('youtube/user-upload/submit', views.submit_user_upload,name="useruploadsubmit"),
    path('youtube/user-channel/videos', views.videos_user_upload,name="showupload"),
    path('youtube/uservideo/<int:id>', views.user_video_playback,name="userplayback"),
    path('youtube/uservideo/remove/<int:id>', views.user_video_remove,name="uservideoremove"),
    path('youtube/comment/<int:video_id>', views.add_comment,name="add_comment"),
    path('youtube/reply/<int:id>', views.reply_comment,name="reply_comment"),
    path('youtube/deletecomment/<int:parent_id>', views.delete_parentcomment,name="delete_parentcomment"),
    path('youtube/deletecomment/child/<int:child_id>', views.delete_childcomment,name="delete_childcomment"),
]