from django.db import models
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from random import randint

from .utils import read_time, count_words
from taggit.managers import TaggableManager
from Topic.models import Category
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify

import logging

logger = logging.getLogger(__name__)


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager,self).get_queryset().filter(status = 'PUBLISHED')

class Article(models.Model):
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"
    STATUS_CHOICES = (
 ('DRAFTED', 'DRAFTED'),
 ('PUBLISHED', 'PUBLISHED'),
 )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,db_index=True )
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name = 'article_post')
    content = RichTextUploadingField()
    publish = models.DateTimeField(default=now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    topics = models.ManyToManyField(Category)
    
    tags = TaggableManager()
    count_words = models.CharField(max_length=100, default=0)
    read_time = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFTED')    
    objects = models.Manager()
    published = PublishManager()    
    class Meta:
        ordering = ['-publish']
        
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.count_words = count_words(self.content)
        self.read_time = read_time(self.content)
        if Article.objects.filter(title = self.title).exists():
            extra = str(randint(1, 1000000))
            self.slug = slugify(self.title) + "-" + extra
        else:
            self.slug = slugify(self.title)
        super(Article, self).save(*args,**kwargs)
     
    
    def get_absolute_url(self):
        return reverse("creo:detail", args= [self.slug])
    
    @property     
    def structured_data(self):
        data = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
             "name": self.title,            
             "author":self.author.username,
             
            
            

        }
        
        return data


    
class Comment(MPTTModel):
 
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
   
    
    class MPTTMeta:
        order_insertion_by = ['created']
        
    def __str__(self):
        return self.content[:17]
            
