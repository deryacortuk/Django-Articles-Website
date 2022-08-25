from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

import logging

logger = logging.getLogger(__name__)

# Create your models here.
class DailyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_daily')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    heart_like = models.IntegerField(default = 0)
    hands_like = models.IntegerField(default = 0)
    star_like = models.IntegerField(default = 0)   
    
    
    
    class Meta:
        ordering = ['-created']
        
    def get_absolute_url(self):
        return reverse("daily:status", args= [self.id])
    
    def __str__(self):
        return self.content[:20]
        
    @property     
    def structured_data(self):
        data = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
             "name": self.user.username,
             "description": self.content,

        }
        
        return data
    
        
class DailyComment(MPTTModel):
    post = models.ForeignKey(DailyModel,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['created']
        
    def __str__(self):
        return self.content[:20]
    
    
    
    
        

  