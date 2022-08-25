
import logging
from django.contrib.postgres import search
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.http.response import HttpResponseBadRequest, JsonResponse
from .models import Article,Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from FollowUser.models import Follow
from Vote.models import Like
from Profil.models import Profile
from Daily.models import DailyModel
from notifications.signals import notify
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.admin.views.decorators import staff_member_required



logger = logging.getLogger(__name__)





class ArticleWriteView(LoginRequiredMixin,View):
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"
    template_name = "Participes/writestory.html"
    context_object = {}
    
    def get(self,request,*args,**kwargs):
        form = ArticleForm()
        self.context_object["form"] = form
        return render(request,self.template_name,self.context_object)
    
    
    
    def post(self, request,*args,**kwargs):
        form = ArticleForm(request.POST,request.FILES)
        action = request.POST.get("action")
        article_status = request.POST["status"]
        if action==self.DRAFTED:
            if article_status == Article.PUBLISHED:
                self.context_object["form"] = form
                messages.info(request,"You try to save the story as draft but selected the status as 'Published'."
                           "Please change the status to 'Drafted' before you save the story as draft."  )
                return render(request,self.template_name,self.context_object)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
                form.save_m2m()
                return redirect("creo:stories",article.author)
            return render(request,self.template_name,self.context_object)
        
        if action == self.PUBLISHED:
            if article_status ==Article.DRAFTED:
               
                self.context_object["form"] = form
                messages.info(request,"You clicked on 'Published' to the story but selected the status as 'Drafted'."
                               "Please change the status to 'Published' before you can publish the story." )
                return render(request,self.template_name,self.context_object)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
                form.save_m2m()
                return redirect("creo:stories",article.author)
                
        self.context_object["form"] = form
        return render(request,self.template_name,self.context_object)
  

@vary_on_cookie
@cache_page(60)  
def stories(request,username):
    user_post = get_object_or_404(User, username = username)
    stories = Article.published.filter(author = user_post)   
    
   
    
    follow = False
    followers = Follow.objects.filter(follower = user_post)[:5]
    followers_count = Follow.objects.filter(follower = user_post).count()
    if request.user.is_authenticated:
        follow = Follow.objects.filter(follower = request.user, following = user_post).exists()
        return render(request,"Participes/stories.html",{'followers_count':followers_count,'stories':stories, 'user_post':user_post, 'follow':follow,'followers':followers} )
    return render(request,"Participes/stories.html",{'followers_count':followers_count,'stories':stories, 'user_post':user_post, 'follow':follow,'followers':followers })


@login_required
def draft_stories(request):
    
    stories = Article.objects.filter(author = request.user, status = "DRAFTED")
 
    return render(request,"Participes/draft.html",{'stories':stories})

@vary_on_cookie
@cache_page(60) 
def detail_story(request,slug):
    
    post = get_object_or_404(Article, slug = slug, status = 'PUBLISHED')
    allcomments = post.comments.all()    
    
    comment_form = CommentForm()
    users = get_object_or_404(User, id = post.author.id)
    followers = Follow.objects.filter(follower = users)[:5]
    heart = Like.objects.filter(article = post, like ='heart')
    star = Like.objects.filter(article = post, like = 'star')
    hands = Like.objects.filter(article = post, like = 'hands') 
    post_tags_ids = post.tags.values_list('id',flat=True)  
    similar_posts = Article.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).exclude(author=request.user).order_by('-same_tags','-publish')[:7]
    
    followers_count = Follow.objects.filter(follower = users).count()  
            
    
    follow = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(follower = request.user, following = users).exists()
        return render(request, "Participes/story_detail.html", {'followers_count':followers_count,'similar_posts':similar_posts,'hands':hands,'heart':heart,'star':star,'post':post, 'comment_form':comment_form,'users':users, 'allcomments':allcomments, 'follow': follow, 'followers':followers})
    return render(request,"Participes/story_detail.html",{'followers_count':followers_count,'similar_posts':similar_posts,'hands':hands,'star':star,'heart':heart,'post':post, 'comment_form': comment_form, 'users':users, 'allcomments':allcomments, 'follow':follow, 'followers':followers })





class ArticleUpdateView(LoginRequiredMixin,View):
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"
    template_name = "Participes/update_story.html"
    context_object = {}
    
    def get(self,request,*args,**kwargs):
        old_article = get_object_or_404(Article, slug = self.kwargs.get("slug"))
        update_article_form = ArticleForm(instance=old_article,initial={'tags':old_article.tags.name})
        self.context_object["update_article_form"] =update_article_form
        self.context_object["article"] = old_article
        return render(request, self.template_name,self.context_object)
    
    def post(self,request,*args,**kwargs):
        old_article = get_object_or_404(Article,slug = self.kwargs.get("slug"))
        update_article_form = ArticleForm(request.POST,request.FILES, instance=old_article)
        
        action = request.POST.get("action")
        article_status = request.POST["status"]
        
        if action == Article.DRAFTED:
            
            if article_status == Article.PUBLISHED:
                self.context_object["update_article_form"] = update_article_form
                messages.info(request,"You try to save the story as draft but selected the status as 'Published'."
                           "Please change the status to 'Drafted' before you save the story as draft.")
                return render(request,self.template_name,self.context_object)
            
            if update_article_form.is_valid():
                article = update_article_form.save(commit=False)
                article.author = request.user
                article.publish = timezone.now()
                article.save()
                update_article_form.save_m2m()
                return redirect("creo:draft")
        if action == self.PUBLISHED:
            
            if article_status == Article.DRAFTED:
                self.context_object["update_article_form"] = update_article_form
                
                messages.info(request, "You clicked on 'Published' to the story but selected the status as 'Drafted'."
                               "Please change the status to 'Published' before you can publish the story.")
                return render(request,self.template_name,self.context_object)
            if update_article_form.is_valid():
                article = update_article_form.save(commit=False)
                article.author = request.user
                article.publish = timezone.now()
                article.save()
                update_article_form.save_m2m()
             
                return HttpResponseRedirect(article.get_absolute_url())
            
        self.context_object["update_article_form"] = update_article_form
        messages.error(request,"Please fill required fields.")
        return render(request,self.template_name,self.context_object)
    
    
@login_required
def delete_story(request,id):
    if request.method =="POST":
        story = Article.objects.get(id=id)
        story.author = request.user
   
        story.delete()
        return JsonResponse(data={"success":"Story was deleted."})
    else:
        
       return HttpResponseBadRequest("invalid request.")

@login_required
def addcomment(request):
    if request.method == "POST":
        if request.POST.get('action') == "delete":
            id = request.POST.get('nodeid')
            ct = Comment.objects.get(id=id)
            ct.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                user_comment  = comment_form.save(commit = False)
                result = comment_form.cleaned_data.get('content')
                user = request.user.username
                user_comment.user = request.user
                user_comment.save()
                if request.user != user_comment.post.author:
                    notify.send(request.user, recipient = user_comment.post.author, verb = "added a comment", target = user_comment.post)
                
                return JsonResponse({'status':'success'})
            return HttpResponseBadRequest('invalid request')


def followuser(request,username):
    user_main = get_object_or_404(User,username= username)
    lw = []
    follow = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(following = user_main, follower = request.user).exists()
        flw = Follow.objects.filter(follower = request.user)
        follower = Follow.objects.filter(following = user_main)
        
        
        for i in flw:
            for j in follower:
                if i.following.id == j.follower.id:
                    lw.append(i.following.id)
    
        return render(request, "Participes/followerpage.html", {'user_main':user_main, 'lw':lw, 'follow':follow})
    
    follower = Follow.objects.filter(following = user_main)
        
        
    return render(request,"Participes/followerpage.html" ,{'follower' : follower, 'user_main': user_main,'follow': follow})

def followinguser(request,username):
    user_main = get_object_or_404(User,username= username)
    lw = []
    follow = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(follower = request.user, following = user_main).exists()
        flw = Follow.objects.filter(follower = request.user)
        follower = Follow.objects.filter(follower = user_main)
        
        
        for i in flw:
            for j in follower:
                if i.following.id == j.following.id:
                    lw.append(i.following.id)
    
        return render(request, "Participes/followpage.html", {'user_main':user_main, 'lw':lw, 'follow':follow,'follower': follower, 'flw':flw})
    
    follower = Follow.objects.filter(follower = user_main)
        
        
    return render(request,"Participes/followpage.html" ,{'follower' : follower, 'user_main': user_main,'follow':follow})

@vary_on_cookie
@cache_page(60*60)
def user_about(request,username):
    user_about = get_object_or_404(User, username = username)
    profile = get_object_or_404(Profile,user = user_about)
    follow = False
    if request.user.is_authenticated:
        follow = Follow.objects.filter(following = user_about, follower = request.user).exists()
        return render(request,"Profile/about.html",{'profile':profile,'user_about':user_about,'follow':follow})
    return render(request,"Profile/about.html",{'profile':profile,'user_about':user_about,'follow':follow})

@login_required
def user_list(request,username):   
    
    user_main = get_object_or_404(User,username = username)
    profile = get_object_or_404(Profile,user = user_main)
    alllist = profile.favorites.all()
    return render(request, 'Profile/lists.html',{'user_main':user_main,'alllist':alllist})

@vary_on_cookie
@cache_page(60)  
def daily_list(request,username):
    
    user_daily = get_object_or_404(User, username=username)
    
    stories = DailyModel.objects.filter(user = user_daily).all()
    
    
    
    follow = False
    followers = Follow.objects.filter(follower = user_daily)[:5]
    followers_count = Follow.objects.filter(follower = user_daily).count()
    if request.user.is_authenticated:
        follow = Follow.objects.filter(follower = request.user, following = user_daily).exists()
        return render(request,"Participes/dailylist.html",{'followers_count':followers_count, 'stories':stories, 'user_daily':user_daily, 'follow':follow,'followers':followers} )
    return render(request,"Participes/dailylist.html",{'followers_count':followers_count, 'stories':stories, 'user_daily':user_daily, 'follow':follow,'followers':followers })

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

def searchpage(request):
    if request.method == "GET":
        query = request.GET.get('q', '')
        search_vector = SearchVector('title','content') 
        search_query = SearchQuery(query)
        results = Article.published.annotate(search=search_vector,  rank = SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
 
    
        return render(request, 'Search/search.html',{'results':results,'query':query})