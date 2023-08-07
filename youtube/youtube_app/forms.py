from django import forms
from .models import user_uploads

class user_files_Form(forms.ModelForm):
    class Meta:
        model=user_uploads
        fields=['video_title', 'video_category', 'video_description', 'video_thumbnail','video_duration', 'video_videofile']