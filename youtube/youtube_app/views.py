from django.shortcuts import render,HttpResponse,redirect,get_list_or_404,get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from .models import video_details,watch_later,user_videos_history,like,dislike,user_uploads,comments
from django.contrib.auth.models import User
from .forms import user_files_Form
from django.contrib.auth import login,logout,authenticate
from django.contrib.sessions.models import Session
from django.db.models import Max, Sum
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone
from django.core import serializers
from django.contrib import messages
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from moviepy.editor import VideoFileClip
from django.utils import timezone
import time,json


def index(request):
    videos=video_details.objects.all()
    form=user_files_Form()
    return render(request,'youtube_app/index.html',{'videos':videos,'form':form})

def videoplayback(request, id):
    play_video = get_object_or_404(video_details, video_id=id)
    max_like=0
    max_dislike=0
    # Update video views count
    play_video.video_views += 1
    play_video.save()
    
    right_videos = video_details.objects.exclude(video_id=id)
    user_liked = False
    user_disliked = False
    is_parent_comments = comments.objects.filter(video=play_video, parent=None).exists()
    
    if request.user.is_authenticated:
        # in history video present
        his_check=user_videos_history.objects.filter(user=request.user,videos=play_video).exists()
        if his_check:
            update_timestamp=user_videos_history.objects.filter(user=request.user,videos=play_video).first()
            update_timestamp.timestamp=timezone.now()
            update_timestamp.save()
        else:
            insert_video=user_videos_history(user=request.user,videos=play_video) 
            insert_video.save()   
        
        user_liked = like.objects.filter(user=request.user, video=play_video).exists()
        user_disliked = dislike.objects.filter(user=request.user, video=play_video).exists()
        
        # Check if user liked or disliked the video
    
    total_likes=like.objects.filter(video=play_video).exists()
    total_dislikes=dislike.objects.filter(video=play_video).exists()
    
    # Get total likes and dislikes for the video
    if total_likes:
        most_like=like.objects.filter(video=play_video).order_by('-total_like').first()
        max_like=most_like.total_like
    if total_dislikes:
        most_dislike=dislike.objects.filter(video=play_video).order_by('-total_dislike').first()
        max_dislike=most_dislike.total_dislike
        
    
    # Fetch parent comments and their replies
    parent_comments = comments.objects.filter(video=play_video, parent=None).order_by('-timestamp')
    
    return render(request, 'youtube_app/playback.html', {
        'video': play_video,
        'right_videos': right_videos,
        'total_like': max_like,
        'total_dislike': max_dislike,
        'like_status': user_liked,
        'dislike_status': user_disliked,
        'parent_comments': parent_comments,
    })
      
    



def category(request,slug):
    if slug=="All":
        return redirect('/')
    else:
     match_videos=video_details.objects.filter(video_category=slug)
     return render(request,'youtube_app/category.html',{'match_videos':match_videos})
 
def search_suggestions(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        search_suggestions=video_details.objects.filter(Q(video_title__icontains=query)|Q(video_category__icontains=query)|Q(video_channelname__icontains=query))
        search_suggestions_list = list(search_suggestions.values())
        response = json.dumps(search_suggestions_list ,default=str)
        return HttpResponse(response)
    
def search(request,param):
    try:
        param = int(param)
        search = video_details.objects.filter(video_id=param)
    except ValueError:
        query = request.GET.get('search', '')
        search = video_details.objects.filter(
            Q(video_title__icontains=query) |
            Q(video_category__icontains=query) |
            Q(video_channelname__icontains=query)
        )
    return render(request,'youtube_app/index.html',{'videos':search})
        
def handlesignup(request):
    if request.method=="POST":
     try:
        fname=request.POST.get('signupfname')
        lname=request.POST.get('signuplname')
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        myuser=User.objects.create_user(uname,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        login_user=authenticate(request,username=uname,password=password)
        if login_user is not None:
            login(request,login_user)
        messages.success(request,"Account Created Successfully")
        return redirect(request.META.get('HTTP_REFERER', '/'))
     except:
         messages.error(request,"Account already Exist")
         return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponse('404 Verification Failed')    
       
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)        
        return redirect('/')
    else:
        return HttpResponse('User Not Found')
    
def handlelogin(request):
    if request.method=="POST":    
        luname=request.POST.get('loginusername')
        lpassword=request.POST.get('loginpassword')
        user=authenticate(request,username=luname,password=lpassword)
        if user is not None:
            login(request,user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request,"Wrong Credentials Try Again")    
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    else:
        return HttpResponse("404 Request Failed")    

        
def watchlater(request,id):
    if request.user.is_authenticated:
        get_video=video_details.objects.filter(video_id=id).first()
        is_video_added=watch_later.objects.filter(user=request.user,videos=get_video).exists()
        if not is_video_added:
         save_video=watch_later(user=request.user,videos=get_video)
         save_video.save()   
         return JsonResponse({'success':True})  
        else:
            return JsonResponse({'success':True}) 
    else:
        messages_json=[]
        messages.error(request,"Login Required For Add To Watch Later")
        for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
        return JsonResponse({'success': False, 'messages': messages_json}) 
                       
    
def show_watch_later(request):
    if request.user.is_authenticated:
        watch_later_videos=watch_later.objects.filter(user=request.user)
        return render(request,'youtube_app/watchlater.html',{'videos':watch_later_videos})    
    else: 
        messages.error(request,"Login Required")
        return redirect(request.META.get('HTTP_REFERER', '/'))  
    
def remove_watch_video(request,id):
    if request.user.is_authenticated:
        del_video=watch_later.objects.filter(user=request.user,videos=id).delete()
        return JsonResponse({'success':True})
    else:
        messages_json=[]
        messages.error(request,"Something Went Wrong")
        for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
        return JsonResponse({'success': False, 'messages': messages_json}) 
       
def history_show(request):
    if request.user.is_authenticated:
        his_video=user_videos_history.objects.order_by('-timestamp')
        return render(request,'youtube_app/history.html',{'videos':his_video})
    else:
        messages.error(request,"Login Required")
        return redirect(request.META.get('HTTP_REFERER', '/'))      
             
             
def history_remove(request,param):
    if param =="1abc745bf-g":
        if request.user.is_authenticated:
         user_videos_history.objects.filter(user=request.user).delete()
         return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.user.is_authenticated:
        get_video=video_details.objects.filter(video_id=param).first()
        user_videos_history.objects.filter(user=request.user,videos=get_video).delete()
        return JsonResponse({'success':True})
    else:
         messages_json=[]
         messages.error(request,"Something Went Wrong")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
          
def like_update(request,id):
    if request.user.is_authenticated:
        final_like=0
        final_dislike=0
        get_id_video=video_details.objects.filter(video_id=id).first()
        is_user_disliked_video=dislike.objects.filter(user=request.user,video=get_id_video).exists()
        if is_user_disliked_video:
            #del user from dislike and update final_dislike
            get_most_dislike=dislike.objects.filter(video=get_id_video).order_by('-total_dislike').first()
            final_dislike=get_most_dislike.total_dislike-1
            get_most_dislike.total_dislike=get_most_dislike.total_dislike-1
            get_most_dislike.save()
            rem_user_from_disliked=dislike.objects.filter(user=request.user,video=get_id_video).delete()
            #check whether video is in liked or not
            check_file_in_like=like.objects.filter(video=get_id_video).exists()
            if check_file_in_like:
                #if present getting max like of video to update final like
                get_max_like=like.objects.filter(video=get_id_video).order_by('-total_like').first()
                final_like=get_max_like.total_like+1
                #setting user
                liked_user=like(user=request.user,video=get_id_video,total_like=get_max_like.total_like+1)
                liked_user.save()
                status="liked"
                request.session['liked-video'+str(id)]=True
                request.session['disliked-video'+str(id)]=False
            else:
                #if video is not liked before set new user with like 1
                liked_user=like(user=request.user,video=get_id_video,total_like=1)
                liked_user.save()
                final_like=1
                status="liked"
                request.session['liked-video'+str(id)]=True
                request.session['disliked-video'+str(id)]=False
                
        else:
            #if user never disliked this video we should check whether any video is in like to update like
            check_video_like=like.objects.filter(user=request.user,video=get_id_video).exists()
            #we are checking this because if user like before we need to do -1 like
            if check_video_like:
                #if video is present get max_like to update it
                get_max_like=like.objects.filter(video=get_id_video).order_by('-total_like').first()
                final_like=get_max_like.total_like-1
                #video is liked but not by user so create user
                get_max_like.total_like=get_max_like.total_like-1
                get_max_like.save()
                #del video like of user
                del_video_like=like.objects.filter(user=request.user,video=get_id_video).delete()
                #now time to get dislike value
                check_video_dislike=dislike.objects.filter(video=get_id_video).exists()
                if check_video_dislike:
                    get_max_dislike=dislike.objects.filter(video=get_id_video).order_by('-total_dislike').first()
                    final_dislike=get_max_dislike.total_dislike
                else:
                    final_dislike=0       
                status="notliked" 
                request.session['liked-video'+str(id)]=False
                request.session['disliked-video'+str(id)]=True
            else:  
                #means video never liked by user also verify id video is liked by other
                check_video_in_like=like.objects.filter(video=get_id_video).exists()
                if check_video_in_like:
                    get_max_like_video=like.objects.filter(video=get_id_video).order_by('-total_like').first()
                    final_like=get_max_like_video.total_like+1
                    first_user_like=like(user=request.user,video=get_id_video,total_like=get_max_like_video.total_like+1)
                    first_user_like.save()
                else: 
                    final_like=1
                    first_user_like=like(user=request.user,video=get_id_video,total_like=1)
                    first_user_like.save()   
                
                status="liked"
                request.session['liked-video'+str(id)]=True
                request.session['disliked-video'+str(id)]=False      
        return JsonResponse({'status':status,'final_like':final_like,'final_dislike':final_dislike})        
                
    else:  
         messages_json=[]
         messages.error(request,"Login Required To Like The Video")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json})           
                       
def dislike_update(request,id):
    if request.user.is_authenticated:
        final_like=0
        final_dislike=0
        get_id_video=video_details.objects.filter(video_id=id).first()
        is_user_liked_video=like.objects.filter(user=request.user,video=get_id_video).exists()
        if is_user_liked_video:
            #del user from like and update final_like
            get_most_like=like.objects.filter(video=get_id_video).order_by('-total_like').first()
            final_like=get_most_like.total_like-1
            get_most_like.total_like=get_most_like.total_like-1
            get_most_like.save()
            rem_user_from_liked=like.objects.filter(user=request.user,video=get_id_video).delete()
            #check whether video is in disliked or not
            check_file_in_dislike=dislike.objects.filter(video=get_id_video).exists()
            if check_file_in_dislike:
                #if present getting max dislike of video to update final dislike
                get_max_dislike=dislike.objects.filter(video=get_id_video).order_by('-total_dislike').first()
                final_dislike=get_max_dislike.total_dislike+1
                #setting user
                disliked_user=dislike(user=request.user,video=get_id_video,total_dislike=get_max_dislike.total_dislike+1)
                disliked_user.save()
                status="disliked"
                request.session['disliked-video'+str(id)]=True
                request.session['liked-video'+str(id)]=False
            else:
                #if video is not disliked before set new user with dislike 1
                disliked_user=dislike(user=request.user,video=get_id_video,total_dislike=1)
                disliked_user.save()
                final_dislike=1
                status="disliked"
                request.session['disliked-video'+str(id)]=True
                request.session['liked-video'+str(id)]=False
                
        else:
            #if user never liked this video we should check whether any video is in dislike to update dislike
            check_video_dislike=dislike.objects.filter(user=request.user,video=get_id_video).exists()
            #we are checking this because if user like before we need to do -1 like
            if check_video_dislike:
                #if video is present get max_dislike to update it
                get_max_dislike=dislike.objects.filter(video=get_id_video).order_by('-total_dislike').first()
                final_dislike=get_max_dislike.total_dislike-1
                #video is disliked but not by user so create user
                get_max_dislike.total_like=get_max_dislike.total_dislike-1
                get_max_dislike.save()
                #del video dislike of user
                del_video_dislike=dislike.objects.filter(user=request.user,video=get_id_video).delete()
                #now time to get like value
                check_video_like=like.objects.filter(video=get_id_video).exists()
                if check_video_like:
                    get_max_like=like.objects.filter(video=get_id_video).order_by('-total_like').first()
                    final_like=get_max_like.total_like
                else:
                    final_like=0       
                status="notdisliked"    
                request.session['disliked-video'+str(id)]=False
                request.session['liked-video'+str(id)]=True
            else:  
                #means video never disliked by anyone
                check_video_in_dislike=dislike.objects.filter(video=get_id_video).exists()
                if check_video_in_dislike:
                    get_max_dislike_video=dislike.objects.filter(video=get_id_video).order_by('-total_dislike').first()
                    final_dislike=get_max_dislike_video.total_dislike+1
                    first_user_dislike=dislike(user=request.user,video=get_id_video,total_dislike=get_max_dislike_video.total_dislike+1)
                    first_user_dislike.save()
                else: 
                    final_dislike=1
                    first_user_dislike=dislike(user=request.user,video=get_id_video,total_dislike=1)
                    first_user_dislike.save() 
                status="disliked"
                request.session['disliked-video'+str(id)]=True
                request.session['liked-video'+str(id)]=False
               
        return JsonResponse({'status':status,'final_like':final_like,'final_dislike':final_dislike})        
                
    else:  
         messages_json=[]
         messages.error(request,"Login Required To Dislike The Video")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
            

def user_upload(request):
    if request.user.is_authenticated:
        form=user_files_Form()
        return render(request,'youtube_app/user_upload.html',{'form':form})
    
def submit_user_upload(request):
 if request.user.is_authenticated:
    if request.method=="POST":
        form=user_files_Form(request.POST,request.FILES)
        if form.is_valid():
            upload_instance = form.save(commit=False)
            upload_instance.user = request.user
            upload_instance.save()
            messages.success(request,"Video Uploaded Successfully")
            return redirect('/youtube/user-channel/videos')

        else:
           messages.success(request,"Something Went Wrong")   
           return redirect('/')
 else:
     messages.success(request,"Something Went Wrong")   
     return redirect('/')
 
           
def videos_user_upload(request):
    user_videos=user_uploads.objects.filter(user=request.user)
    return render(request,'youtube_app/user_videos.html',{'videos':user_videos})   

def user_video_playback(request,id):
    play_video=user_uploads.objects.filter(video_id=id).first()
    play_video.video_views=play_video.video_views+1
    play_video.save()
    right_videos=user_uploads.objects.exclude(video_id=id)
    return render(request,'youtube_app/user_video_playback.html',{'video':play_video,'right_videos':right_videos})
         
        
def user_video_remove(request,id):
    if request.user.is_authenticated:
        rem_video=user_uploads.objects.filter(video_id=id).delete()
        return JsonResponse({'success':True})
    else:
         messages_json=[]
         messages.error(request,"Something Went Wrong")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
                   
def add_comment(request,video_id):
    if request.user.is_authenticated:
     if request.method=="POST":
      content=request.POST.get('parent-comment')
      get_video=video_details.objects.filter(video_id=video_id).first() 
      new_comment=comments(user=request.user,video=get_video,content=content)
      new_comment.save()
      timestamp=naturaltime(new_comment.timestamp)
      return JsonResponse({'success':True,'user':request.user.username,'comment':new_comment.content,'timestamp':timestamp,'parent_id':new_comment.id})
    else:
         messages_json=[]
         messages.error(request,"Login Required To Add a Comment")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
                         
    
def reply_comment(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            reply_comment=request.POST.get('reply_content')
            parent_id=request.POST.get('parent_id')
            parent_comment = comments.objects.get(id=parent_id)
            get_video=video_details.objects.filter(video_id=id).first()
            user_reply=comments(user=request.user,video=get_video,content=reply_comment,parent=parent_comment)
            user_reply.save()
            timestamp=naturaltime(user_reply.timestamp)
            return JsonResponse({'success':True,'user':request.user.username,'comment':user_reply.content,'timestamp':timestamp,'child_id':user_reply.id})
    else:
         messages_json=[]
         messages.error(request,"Login Required To Reply a Comment")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
     
def delete_parentcomment(request,parent_id):
    if request.user.is_authenticated:
        comment=comments.objects.filter(user=request.user,id=parent_id).exists()
        if comment or request.user.username=="admin287":
         del_comment=comments.objects.filter(id=parent_id).delete()
         return JsonResponse({'success':True})
        else:
         messages_json=[]
         messages.error(request,"You are not authorized user to delete this Comment")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
    else:
         messages_json=[]
         messages.error(request,"Login Required To Reply a Comment")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
        
def delete_childcomment(request,child_id):
    if request.user.is_authenticated:  
       child_comment=comments.objects.filter(user=request.user,id=child_id).exists()
       if child_comment or request.user.username=="admin287":
           delete_child_comment=comments.objects.filter(id=child_id).delete()
           return JsonResponse({'success':True})
       else:    
         messages_json=[]
         messages.error(request,"You are not authorized user to delete this Comment")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json}) 
    else:
         messages_json=[]
         messages.error(request,"Login Required To Reply a Comment")
         for message in messages.get_messages(request):
            messages_json.append({
                'message':message.message,
                'tags':message.tags,
            })
         return JsonResponse({'success': False, 'messages': messages_json})        
                            
               
           
           
       
                    
                    
                    
                
            
            
# Create your views here.
