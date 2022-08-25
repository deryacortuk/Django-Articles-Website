from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from .models import BrandModel, BrandEntry
from .forms import BrandForm
from django.http.response import HttpResponseBadRequest, JsonResponse
from Vote.models import BrandLike
from Profil.models import Profile
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie



@vary_on_cookie
@cache_page(60) 
def brandpage(request,slug):
    brand = get_object_or_404(BrandModel, slug=slug)
    brand_comments = BrandEntry.objects.filter(brand=brand)
    brandfollower = Profile.objects.filter(brandfollow = brand).count()       
            
                        
    
    form = BrandForm()
    
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            user_comment = form.save(commit=False)
            user_comment.user = request.user
            user_comment.brand = brand
            user_comment.save()
            form = BrandForm()
            return render(request,"Porta/brandpage.html",{'brandfollower':brandfollower,'brand':brand,'form':form,'brand_comments':brand_comments})
    return render(request, "Porta/brandpage.html", {'brandfollower':brandfollower,'brand':brand,'form':form,'brand_comments':brand_comments})


  
    
    
@login_required
def delete_comment(request,id):
    if request.method =="POST":
        comment = BrandEntry.objects.get(id=id)
        comment.user = request.user
   
        comment.delete()
        return JsonResponse(data={"success":"Story was deleted."})
    else:
        
       return HttpResponseBadRequest("invalid request.")
        
        


    
    
          
        


