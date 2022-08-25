from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls.base import reverse,reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Brand.models import BrandModel
from Profil.models import Profile
from Profil.forms import ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from Participes.models import Article
from django.views.decorators.csrf import csrf_exempt
from Topic.models import Category
import logging

logger = logging.getLogger(__name__)


@login_required
def profilepage(request):
    
    profile = get_object_or_404(Profile,user=request.user)
    
    
    return render(request,"Profile/profile.html",{'profile':profile})


@login_required
def profileuser(request):
    profile = get_object_or_404(Profile,user = request.user)
    
    form = ProfileForm(instance = profile)
    
    if request.method =="POST":
        form = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('profile:me'))
        else:
            return render(request,'Profile/profile_edit.html',{'form':form})
    return render(request,'Profile/profile_edit.html',{'form':form})

class PasswordsChangeView(PasswordChangeView):
    form_class =PasswordChangeForm
    success_url = reverse_lazy('profile:passwordsuccess')

@login_required
def password_success(request):
    return render(request,'Profile/passwordsuccess.html',{})

@login_required
@csrf_exempt
def add_list(request,id):
    if request.method == "POST":
        article = get_object_or_404(Article,id = id)
        request.user.profile.favorites.add(article)
        return JsonResponse({'status':'success'})
    
@login_required
@csrf_exempt
def remove_list(request,id):
    if request.method == "POST":
        article = get_object_or_404(Article, id=id)
        request.user.profile.favorites.remove(article)
        return JsonResponse({'status':'success'})

        
@login_required
@csrf_exempt
def add_topic(request,id):
    if request.method == "POST":
        
        topic = get_object_or_404(Category, id=id)
        request.user.profile.interest.add(topic)
        return JsonResponse({'status':'success'})
    
@login_required
@csrf_exempt
def remove_topic(request,id):
    if request.method == "POST":
        
        topic = get_object_or_404(Category,id=id)
        request.user.profile.interest.remove(topic)
        return JsonResponse({'status':'success'})
@login_required
@csrf_exempt
def brand_follow(request,id):
    if request.method == "POST":
        brand = get_object_or_404(BrandModel,id=id)
        request.user.profile.brandfollow.add(brand)
        return JsonResponse({'status':'success'})
@login_required
@csrf_exempt
def remove_follow(request, id):
    if request.method == "POST":
        brand = get_object_or_404(BrandModel,id = id)
        request.user.profile.brandfollow.remove(brand)
        return JsonResponse({'status':'success'})
        
    
    

        

        


