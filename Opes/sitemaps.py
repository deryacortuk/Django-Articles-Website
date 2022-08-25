import re
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse
from Brand.models import BrandModel, BrandEntry
from Daily.models import DailyModel, DailyComment
from Participes.models import Article, Comment

from Topic.models import Category
from Profil.models import Profile
from taggit.models import Tag

class StaticViewSitemap(Sitemap):
    priority = "0.5"
    changefreg = "montly"
    
    def items(self):
        return ['porro:gateway','porro:topics','porro:brands','porro:about','porro:share','porro:contact']
    
    def location(self, item):
        return reverse(item)
    
class ArticleSiteMap(Sitemap):
    changefreg = "weekly"
    priority = "0.7"
    
    def items(self):
        return Article.published.all()
    def lastmod(self, obj):
        return obj.publish
    
    
class CategorySiteMap(Sitemap):
    changefreg = "montly"
    priority = "0.8"
    
    def items(self):
        return Category.objects.all()
    
  

    
class DailySiteMap(Sitemap):
    changefreg = "daily"
    priority = "0.8"
    def items(self):
        return DailyModel.objects.all()
    def lastmod(self,obj):
        return obj.created
    
class BrandSiteMap(Sitemap):
    changefreg = "weekly"
    priority = "0.7"
    def items(self):
        return BrandModel.objects.all()
    

    
class UserProfileSiteMap(Sitemap):
    changefreg = "daily"
    priority = "0.7"
    def items(self):
        return Profile.objects.all()
    

    
