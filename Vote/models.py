from django.db import models
from Participes.models import Article,Comment
from django.contrib.auth.models import User
from Brand.models import BrandEntry
from Daily.models import DailyModel, DailyComment



class Like(models.Model):
    LIKES = (
        ('hands','hands'),
        ('heart','heart'),
        ('star','star')
    )
    
    article = models.ForeignKey(Article, related_name='article_vote',on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_vote', on_delete=models.CASCADE)
    like = models.CharField(max_length = 255, choices=LIKES)
    

   
    articlecomment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='articlecomment', null=True, blank=True)
    
  
        
   
    
class DailyLike(models.Model):
    LIKES = (
        ('hands','hands'),
        ('heart','heart'),
        ('star','star')
    )
    
    
    user = models.ForeignKey(User, related_name='uservote', on_delete=models.CASCADE)
    like = models.CharField(max_length = 255, choices=LIKES)  
    
    dailyd = models.ForeignKey(DailyModel, on_delete=models.CASCADE, related_name='daily_vote', null= True, blank=True)
    dailycomment = models.ForeignKey(DailyComment, on_delete=models.CASCADE, related_name='dailycomment', null = True, blank=True)
    
   
    
class BrandLike(models.Model):
    LIKES = (
        ('hands','hands'),
        ('heart','heart'),
        ('star','star')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userlike")
    brandlike = models.ForeignKey(BrandEntry, on_delete=models.CASCADE,related_name='brand_vote')
    like = models.CharField(max_length = 255, choices=LIKES)
   
    
   
    
    
    
    


    

