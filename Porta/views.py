
from django.shortcuts import render,get_object_or_404
from Participes.models import Article
from Profil.models import Profile
from Topic.models import Category
from FollowUser.models import Follow
from django.contrib.auth.models import User
from Brand.models import BrandModel
from Daily.models import DailyModel, DailyComment
from Daily.forms import DailyForm, CommentDailyForm
from django.core.mail import send_mail
from Vote.models import Like
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Count




def index(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User,username = request.user)
        
        daily = DailyModel.objects.filter(user = user)
        
        
        following = Follow.objects.filter(follower = user)       
        
        topics = user.profile.interest.all() 
        
        recommend_articles =Article.published.filter(topics__in = topics).exclude(author=user)   
        recommend_articles = recommend_articles.annotate(same_topics = Count('topics')).order_by('-same_topics','-publish')[:20]
        
        
        
        followers = Follow.objects.filter(follower_id = user).values_list('following_id', flat=True)
        posts = Article.published.filter(author_id__in = followers).order_by('-publish')
        
        most_populars = Article.published.annotate(num_likes = Count('article_vote')).exclude(author=user).order_by('-num_likes')
        
        most_followers = User.objects.annotate(popular = Count('following')).exclude(username=user).order_by('-popular')[:10]
        
        
        
        
      
        
        form = DailyForm()                
                        
                                  
        
        return render(request,'Participes/domum.html', {'most_followers':most_followers,'most_populars':most_populars,'followers':followers,'posts':posts,'recommend_articles':recommend_articles,'following' :following,'topics':topics , 'daily':daily,'form':form})    
                     
    else:    
        return render(request,"Porta/index.html" )  
    
@vary_on_cookie
@cache_page(60*60)
def brands(request):
    brands = BrandModel.objects.all()
    return render(request,"Porta/brands.html", {'brands':brands})

@vary_on_cookie
@cache_page(60)
def topics(request):
    topics = Category.objects.all()
    return render(request,"Porta/topics.html", {'topics':topics})

@vary_on_cookie
@cache_page(60*60)
def ourstory(request):
    return render(request,"Porta/ourstory.html")

@vary_on_cookie
@cache_page(60*60)
def write(request):
    return render(request,"Porta/write.html")

def contact(request):
    if request.method == "POST":
        message_name = request.POST['name']
        message_email = request.POST['email']
        message_content = request.POST['message']
        
        send_mail(
            message_name, 
            message_content ,             
             message_email, 
                 
            ['deryacortuk@gmail.com'],
        )
        message = "Thank you for contacting us.Your message has been successfully sent. We will contact you very soon! "
        return render(request, 'Porta/contact.html',{'message':message})
        
    return render(request,'Porta/contact.html',{})


def handler_not_found(request,exception):
    return render(request,'404.html')

def handler_server_error(request):
    return render(request,'500.html')


    
def handler_400(request,exception):
    return render(request, '400.html', status=400)

def handler403(request,exception):
    return render(request, '403.html', status=403)
