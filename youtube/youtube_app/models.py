from django.db import models
from django.contrib.auth.models import User



class video_details(models.Model):
    video_id=models.AutoField(primary_key=True)
    video_title=models.CharField(max_length=150)
    video_category=models.CharField(max_length=100)
    video_description=models.TextField(default="")
    video_thumbnail=models.ImageField(upload_to='thumbnail')
    video_channelname=models.CharField(max_length=100,default="")
    video_timestamp=models.DateTimeField(auto_now_add=True)
    video_duration=models.CharField(max_length=20,default="")
    video_views=models.IntegerField(default=0)
    video_videofile=models.FileField(upload_to='video')
    def __str__(self):
        return self.video_title
    
class watch_later(models.Model):    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    videos=models.ForeignKey(video_details,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
    
class like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(video_details,on_delete=models.CASCADE)    
    total_like=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    
class dislike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(video_details,on_delete=models.CASCADE)    
    total_dislike=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    
class user_uploads(models.Model):
    video_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,null=True, blank=True,on_delete=models.CASCADE)
    video_title=models.CharField(max_length=150)
    video_category=models.CharField(max_length=100)
    video_description=models.TextField(default="")
    video_thumbnail=models.ImageField(upload_to='upload_thumbnail')
    video_timestamp=models.DateTimeField(auto_now_add=True)
    video_duration=models.CharField(max_length=20,default="")
    video_views=models.IntegerField(default=0)
    video_videofile=models.FileField(upload_to='upload')
    def __str__(self):
        return self.user.username
    
class user_videos_history(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    videos=models.ForeignKey(video_details,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username+self.videos.video_title
    
    
class comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.ForeignKey(video_details,on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)  
    def __str__(self):
        return f"Comment By {self.user.username}-{self.content}"  
    
   
        
    


# Create your models here.
