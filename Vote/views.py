
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from Participes.models import Article, Comment
from Vote.models import Like, DailyLike, BrandLike
from Brand.models import BrandEntry
from Daily.models import DailyComment, DailyModel
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify


@login_required
@never_cache
@csrf_exempt
def likeArticle(request, id):
    if request.method == "POST":
        user = request.user
        post = Article.published.get(id = id)
        profile = get_object_or_404(User,username = user)
        
        action = request.POST.get('action', '')
        liked = Like.objects.filter(article = post, user = profile).count()
        
        if not liked:
            if action == 'heart':
                Like.objects.get_or_create(article = post, user = profile, like = 'heart')
                
               
                if request.user != post.author:
                    notify.send(request.user, recipient = post.author, verb="has liked",target= post  )
            elif action == 'star':
                Like.objects.get_or_create(article = post, user = profile, like = 'star')
                if request.user != post.author:
                    notify.send(request.user, recipient = post.author, verb="has liked",target=post)
            elif action == 'hands':
                Like.objects.get_or_create(article = post, user = profile, like ='hands')
                if request.user != post.author:
                    notify.send(request.user, recipient = post.author, verb="has liked",target =post)
            
            else:
                return HttpResponseBadRequest('invalid')
            
            
            heart = Like.objects.filter(article = post, like = 'heart').count()
            hands = Like.objects.filter (article = post, like = 'hands').count()
            star = Like.objects.filter(article= post, like = 'star').count()
            return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
        
        else:
            if action == 'hands':
                hands = Like.objects.filter(article = post, user = profile, like = 'hands').count()
                
                if hands:
                    Like.objects.filter(article = post, user = profile).delete()
                else:
                    Like.objects.filter(article= post, user = profile).delete()
                    Like.objects.get_or_create(article = post, user = profile, like = 'hands')
                    if request.user != post.author:
                        notify.send(request.user, recipient = post.author, verb="has liked",target=post)
                
                heart = Like.objects.filter(article = post, like = 'heart').count()
                hands = Like.objects.filter (article = post, like = 'hands').count()
                star = Like.objects.filter(article= post, like = 'star').count()
                return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
            
            elif action == 'star':
                star = Like.objects.filter(article = post, user = profile, like = 'star').count()
                
                if star:
                    Like.objects.filter(article = post, user = profile).delete()
                else:
                    Like.objects.filter(article = post, user = profile).delete()
                    Like.objects.get_or_create(article = post, user = profile, like = 'star')
                    if request.user != post.author:
                        notify.send(request.user, recipient = post.author, verb="has liked",target=post)
                    
                heart = Like.objects.filter(article = post, like = 'heart').count()
                hands = Like.objects.filter (article = post, like = 'hands').count()
                star = Like.objects.filter(article= post, like = 'star').count()
                return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
            
            elif action == 'heart':
                heart = Like.objects.filter(article = post, user = profile,like = 'heart').count()
                
                if heart:
                    Like.objects.filter(article = post, user = profile).delete()
                else:
                    Like.objects.filter(article = post, user = profile).delete()
                    Like.objects.get_or_create(article = post, user = profile, like = 'heart')
                    if request.user != post.author:
                        notify.send(request.user, recipient = post.author, verb="has liked ",target=post)
                heart = Like.objects.filter(article = post, like = 'heart').count()
                hands = Like.objects.filter (article = post, like = 'hands').count()
                star = Like.objects.filter(article= post, like = 'star').count()
                return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
            
            else:
                return HttpResponseBadRequest('invalid request')
            
@login_required       
@never_cache
@csrf_exempt      
def articlecommentlike(request,id):
    
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(User, username = user)
        comment = get_object_or_404(Comment, id = id)
        
        action = request.POST.get('action')
        
        liked = Like.objects.filter(user = profile, articlecomment = comment).count()
        
        if not liked:
            
            if action == 'hands':
                Like.objects.get_or_create(user = profile, articlecomment = comment, like = 'hands')
                if request.user != comment.user:
                        notify.send(request.user, recipient = comment.user, verb="has liked your comment",target=comment)
            
            handss = Like.objects.filter(articlecomment = comment, like = 'hands').count()
            return JsonResponse({'handss':handss})
        else:
            handss = Like.objects.filter(articlecomment = comment, user =profile, like = 'hands').delete()
        
        handss = Like.objects.filter(articlecomment = comment, like = 'hands').count()
        handslist = Like.objects.filter(articlecomment=comment, like = 'hands')
        return JsonResponse({'handss':handss,'handslist':handslist})
    
    
@login_required
@never_cache
@csrf_exempt
def likeDaily(request, id):
    if request.method == "POST":
        user = request.user
        postd = DailyModel.objects.get(id = id)
        profile = get_object_or_404(User,username = user)
        
        action = request.POST.get('action', '')
        liked = DailyLike.objects.filter(dailyd = postd, user = profile).count()
        
        
        if not liked:
            if action == 'heart':
                DailyLike.objects.get_or_create(dailyd = postd, user = profile, like = 'heart')
                postd.heart_like = DailyLike.objects.filter(dailyd = postd, user = profile, like = 'heart').count()
                postd.save()
                if request.user != postd.user:
                    notify.send(request.user, recipient = postd.user, verb="has liked your post",target =postd)
                    
            elif action == 'star':
                DailyLike.objects.get_or_create(dailyd = postd, user = profile, like = 'star')
                postd.star_like = DailyLike.objects.filter(dailyd = postd, user = profile, like = 'star').count()
                postd.save()
                if request.user != postd.user:
                    notify.send(request.user, recipient = postd.user, verb="has liked your post",target =postd)
                    
            elif action == 'hands':
                DailyLike.objects.get_or_create(dailyd = postd, user = profile, like ='hands')
                postd.hands_like = DailyLike.objects.filter(dailyd = postd, user = profile, like = 'hands').count()
                postd.save()
                if request.user != postd.user:
                    notify.send(request.user, recipient = postd.user, verb="has liked your post",target =postd)
            
            else:
                return HttpResponseBadRequest('invalid')
            
            
            postd.heart_like = DailyLike.objects.filter(dailyd = postd, like = 'heart').count()
            postd.hands_like = DailyLike.objects.filter(dailyd = postd,  like = 'hands').count()
            postd.star_like = DailyLike.objects.filter(dailyd = postd, like = 'star').count()
            postd.save()
            heart = postd.heart_like
            hands = postd.hands_like
            star = postd.star_like
            return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
        
        else:
            if action == 'hands':
                hands = DailyLike.objects.filter(dailyd = postd, user = profile, like = 'hands').count()
                
                if hands:
                    DailyLike.objects.filter(dailyd = postd, user = profile).delete()
                else:
                    DailyLike.objects.filter(dailyd = postd, user = profile).delete()
                    DailyLike.objects.get_or_create(dailyd = postd, user = profile, like = 'hands')
                    if request.user != postd.user:
                        notify.send(request.user, recipient = postd.user, verb="has liked your post",target =postd)
                
              
                postd.heart_like = DailyLike.objects.filter(dailyd = postd, like = 'heart').count()
                postd.hands_like = DailyLike.objects.filter(dailyd = postd,  like = 'hands').count()
                postd.star_like = DailyLike.objects.filter(dailyd = postd, like = 'star').count()
                postd.save()
                heart = postd.heart_like
                hands = postd.hands_like
                star = postd.star_like
                return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
            
            elif action == 'star':
                star = DailyLike.objects.filter(dailyd = postd, user = profile, like = 'star').count()
                
                if star:
                    DailyLike.objects.filter(dailyd = postd, user = profile).delete()
                else:
                    DailyLike.objects.filter(dailyd = postd, user = profile).delete()
                    DailyLike.objects.get_or_create(dailyd = postd, user = profile, like = 'star')
                    if request.user != postd.user:
                        notify.send(request.user, recipient = postd.user, verb="has liked your post",target =postd)
                    
               
                postd.heart_like = DailyLike.objects.filter(dailyd = postd, like = 'heart').count()
                postd.hands_like = DailyLike.objects.filter(dailyd = postd,  like = 'hands').count()
                postd.star_like = DailyLike.objects.filter(dailyd = postd, like = 'star').count()
                postd.save()
                heart = postd.heart_like
                hands = postd.hands_like
                star = postd.star_like
                return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
            
            elif action == 'heart':
                heart = DailyLike.objects.filter(dailyd = postd, user = profile,like = 'heart').count()
                
                if heart:
                    DailyLike.objects.filter(dailyd = postd, user = profile).delete()
                else:
                    DailyLike.objects.filter(dailyd = postd, user = profile).delete()
                    DailyLike.objects.get_or_create(dailyd = postd, user = profile, like = 'heart')
                    
                    if request.user != postd.user:
                        notify.send(request.user, recipient = postd.user, verb="has liked your post",target =postd)
                    
               
                postd.heart_like = DailyLike.objects.filter(dailyd = postd, like = 'heart').count()
                postd.hands_like = DailyLike.objects.filter(dailyd = postd,  like = 'hands').count()
                postd.star_like = DailyLike.objects.filter(dailyd = postd, like = 'star').count()
                postd.save()
                heart = postd.heart_like
                hands = postd.hands_like
                star = postd.star_like
                return JsonResponse({'star':star, 'heart':heart, 'hands':hands})
            
            else:
                return HttpResponseBadRequest('invalid request')
            
            
@login_required       
@never_cache
@csrf_exempt      
def dailycommentlike(request,id):
    
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(User, username = user)
        comment = get_object_or_404(DailyComment, id = id)
        
        action = request.POST.get('action', '')
        
        liked = DailyLike.objects.filter(user = profile, dailycomment = comment).count()
        
        if not liked:
            
            if action == 'hands':
                DailyLike.objects.get_or_create(user = profile, dailycomment = comment, like = 'hands')
                if request.user != comment.user:
                        notify.send(request.user, recipient = comment.user, verb="has liked your comment",target = comment)
                
                
            
            hands = DailyLike.objects.filter(dailycomment = comment, like = 'hands').count()
            return JsonResponse({'hands':hands})
        else:
            hands = DailyLike.objects.filter(dailycomment = comment, user =profile, like = 'hands').delete()
        
        hands = DailyLike.objects.filter(dailycomment = comment, like = 'hands').count()
        return JsonResponse({'hands':hands})
            
            
@login_required
@never_cache
@csrf_exempt
def brandcommentlike(request,id):
    
    user = request.user
    
    profile = get_object_or_404(User, username = user)
    brand = get_object_or_404(BrandEntry, id = id)
    
    action = request.POST.get('action','')
    
    liked = BrandLike.objects.filter(user = profile, brandlike = brand).count()
    
    if not liked:
        if action == 'hands':
            BrandLike.objects.get_or_create(user = profile, brandlike = brand, like = 'hands')
            brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
            brand.save()
            if request.user != brand.user:
                        notify.send(request.user, recipient = brand.user, verb="has liked your comment",target =brand)
            
            
        elif action == 'star':
            BrandLike.objects.get_or_create(user = profile,brandlike = brand, like = 'star')
            brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
            brand.save()
            if request.user != brand.user:
                        notify.send(request.user, recipient = brand.user, verb="has liked your comment",target =brand)
        elif action == 'heart':
            BrandLike.objects.get_or_create(user = profile,brandlike = brand, like = 'heart')
            brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
            brand.save()
            if request.user != brand.user:
                        notify.send(request.user, recipient = brand.user, verb="has liked your comment",target =brand)
            
        else:
            return HttpResponseBadRequest('invalid request')
        
        brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
        brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
        brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
        brand.save()
        heart = brand.heart_like    
        hands = brand.hands_like     
        star =  brand.star_like  
        return JsonResponse({'star':star, 'heart':heart,'hands':hands})
    
    else:
        if action == 'hands':
            hands = BrandLike.objects.filter(brandlike = brand,user = profile, like = 'hands').count()
            
            if hands:
                BrandLike.objects.filter(brandlike = brand,user = profile).delete()
                
            else:
                BrandLike.objects.filter(brandlike = brand, user = profile).delete()
                BrandLike.objects.get_or_create(brandlike = brand, user = profile, like = 'hands')
                brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
                brand.save()
                if request.user != brand.user:
                        notify.send(request.user, recipient = brand.user, verb="has liked your comment",target =brand)
             
            brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
            brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
            brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
            brand.save()
            heart = brand.heart_like    
            hands = brand.hands_like     
            star =  brand.star_like   
        
            return JsonResponse({'star':star, 'heart':heart,'hands':hands})
        
        elif action == 'heart':
            heart = BrandLike.objects.filter(brandlike = brand, user = profile, like = 'heart').count()
            
            if heart:
                BrandLike.objects.filter(brandlike = brand, user = profile).delete()
            else:
                BrandLike.objects.filter(brandlike = brand, user = profile).delete()
                BrandLike.objects.get_or_create(brandlike = brand, user = profile, like = 'heart')
                brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
                brand.save()
                if request.user != brand.user:
                        notify.send(request.user, recipient = brand.user, verb="has liked your comment",target =brand)
                
           
            
            brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
            brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
            brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
            brand.save()
            heart = brand.heart_like    
            hands = brand.hands_like     
            star =  brand.star_like  
        
            return JsonResponse({'star':star, 'heart':heart,'hands':hands})
        
        elif action == 'star':
            star = BrandLike.objects.filter(brandlike = brand, user = profile, like = 'star').count()
            
            if star:
                BrandLike.objects.filter(brandlike = brand, user = profile).delete()
            else:
                BrandLike.objects.filter(brandlike = brand, user = profile).delete()
                BrandLike.objects.get_or_create(brandlike = brand, user = profile, like = 'star')
                brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
                brand.save()
                if request.user != brand.user:
                        notify.send(request.user, recipient = brand.user, verb="has liked your comment",target =brand)
                
            
            brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
            brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
            brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
            brand.save()
            heart = brand.heart_like    
            hands = brand.hands_like     
            star =  brand.star_like  
       
            return JsonResponse({'star':star, 'heart':heart,'hands':hands})
        
        else:
            
            
            brand.heart_like = BrandLike.objects.filter(brandlike = brand, like = 'heart').count()
            brand.hands_like = BrandLike.objects.filter(brandlike = brand, like = 'hands').count()
            brand.star_like = BrandLike.objects.filter(brandlike = brand, like = 'star').count()
            brand.save()
            heart = brand.heart_like    
            hands = brand.hands_like     
            star =  brand.star_like   
        
            return JsonResponse({'star':star, 'heart':heart,'hands':hands})
        
  
                

        
                
                
                
            
            
        
              
            
    
    
