from django.shortcuts import render,get_object_or_404

from Profil.models import Profile
from .models import Category
from Participes.models import Article
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie



@vary_on_cookie
@cache_page(60*15) 
def topic(request,slug):
    topic = get_object_or_404(Category,slug = slug)
    stories = Article.published.filter(topics = topic).order_by('-publish') 
    followers = Profile.objects.filter(interest = topic).count()
    
   
    
    return render(request,"Topic/topic.html",{'topic':topic,'stories':stories,'followers':followers})
    
