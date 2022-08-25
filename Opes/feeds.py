from django.contrib.syndication.views import Feed
from django.urls.base import reverse
from Participes.models import Article
from django.conf import settings
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils.feedgenerator import Atom1Feed

class ArticleFeed(Feed):
    
    feed_type = Rss201rev2Feed
    description = "Social Networking Platform"
    title = "Article site"
    link = "/feed/"

    
    def items(self):
        return Article.published.all().order_by('-publish')[:10]
    
    def item_title(self,item):
        return item.title 
   
    def item_link(self, item):
        return item.get_absolute_url()
    def item_guid(self,item):
        return
    
class AtomSiteNewsFeed(ArticleFeed):
     feed_type = Atom1Feed
     subtitle = ArticleFeed.description
    
    
    
    