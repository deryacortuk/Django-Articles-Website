from django.dispatch.dispatcher import receiver
from django.shortcuts import render, get_object_or_404
from .models import DailyModel
from .forms import DailyForm,CommentDailyForm

from django.http.response import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DailyComment
from django.contrib.auth.models import User
from FollowUser.models import Follow
from Vote.models import DailyLike, Like
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify
from django.db.models import Count
from Participes.models import Article
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
# Create your views here.


@login_required
def dailycomment(request):
    if request.method == "POST":
        form = DailyForm(request.POST)
        if form.is_valid():
            daily_comment = form.save(commit= False)
            daily_comment.user = request.user
            user = request.user.username                     
            
            daily_comment.save()
            return JsonResponse({'user':user})
        return HttpResponseBadRequest('invalid request')
    
@login_required
def deletecomment(request,id):
    if request.method == "POST":
        daily = DailyModel.objects.get(id=id)
        daily.user = request.user
        daily.delete()
        return JsonResponse({"success":"Story was deleted."} )
    else:
        return HttpResponseBadRequest('invalid request')
    
@login_required
def delete_comment(request,id):
    if request.method == "POST":
        daily = DailyComment.objects.get(id=id)
        daily.user = request.user
        daily.delete()
        return JsonResponse({"success":"Story was deleted."} )
    else:
        return HttpResponseBadRequest('invalid request')
    
@login_required
@csrf_exempt
def comment_added(request):
    if request.method == "POST":
        comment_form = CommentDailyForm(request.POST)
        if comment_form.is_valid():
            comment_user = comment_form.save(commit=False)
            comment_user.user = request.user
            result = comment_form.cleaned_data.get('content')
            user = request.user.username
            comment_user.save()
            if request.user != comment_user.post.user:
                
                notify.send(request.user, recipient = comment_user.post.user, verb = "added a comment", target = comment_user.post)
            
            
            return JsonResponse({'result':result,'user':user})
        return HttpResponseBadRequest('invalid')
          
@vary_on_cookie
@cache_page(60)       
def dailystatus(request,id):
    post = get_object_or_404(DailyModel,id=id)
    allcomments = post.comments.all()
    comment_form = CommentDailyForm()
    
    heart = DailyLike.objects.filter(dailyd = post, like = 'heart')
    hands = DailyLike.objects.filter(dailyd = post, like = 'hands')
    star = DailyLike.objects.filter(dailyd = post, like = 'star')
    post.heart_like = DailyLike.objects.filter(dailyd = post, like = 'heart').count()
    post.hands_like = DailyLike.objects.filter(dailyd = post, like = 'hands').count()
    post.star_like = DailyLike.objects.filter(dailyd = post, like = 'star').count()
    post.save()
    
    lw = []
    users = get_object_or_404(User, id = post.user.id)
    followers = Follow.objects.filter(follower = users)[:5]
    followers_count =Follow.objects.filter(follower = users).count()
    
    follow = False
    if request.user.is_authenticated:
        topics = request.user.profile.interest.all()
        recommend_articles =Article.published.filter(topics__in = topics).exclude(author=request.user)   
        recommend_articles = recommend_articles.annotate(same_topics = Count('topics')).exclude(author=request.user).order_by('-same_topics','-publish')[:7]
        follow = Follow.objects.filter(follower = request.user, following = users).exists()
        user_follow = Follow.objects.filter(follower = request.user)
        for i in user_follow:
            lw.append(i.following.id)       
        
        
        
        return render(request, 'Daily/daily.html',{'recommend_articles':recommend_articles,'followers_count':followers_count, 'hands':hands,'star':star,'lw':lw,'heart':heart,'post':post,'users':users,'followers':followers,'allcomments':allcomments,'follow':follow, 'comment_form':comment_form})
    
    return render(request, 'Daily/daily.html',{'followers_count':followers_count,'hands':hands,'star':star,'lw':lw,'heart':heart,'post':post,'follow':follow,'users':users,'allcomments':allcomments, 'comment_form':comment_form})
   
            
        




            