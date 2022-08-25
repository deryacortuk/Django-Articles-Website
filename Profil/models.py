from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
import os
from Topic.models import Category
from Participes.models import Article
from Brand.models import BrandModel
import logging

logger = logging.getLogger(__name__)


def user_directory_path(instance, filename):
    
    profile_pic_name = 'user_{0}/profile.png'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT,profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to = user_directory_path,blank = True, null= True, verbose_name='Picture')
    bio = models.CharField(max_length=500,blank=True, null = True)
    linkedin_url = models.URLField(blank=True, null=True, verbose_name='linkedin')
    twitter_url = models.URLField(blank=True, null=True,verbose_name='twitter')
    facebook_url = models.URLField(blank=True,null=True,verbose_name='facebook')
    instagram_url = models.URLField(blank=True, null=True,verbose_name='instagram')
    interest = models.ManyToManyField(Category)
    favorites = models.ManyToManyField(Article)
    brandfollow = models.ManyToManyField(BrandModel)
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250
        if self.image:
            pic = Image.open(self.image.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.image.path)
            
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property     
    def structured_data(self):
        data = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
             "name": self.user.username,
             
             "description": self.bio,
             
            
            

        }
        
        return data
