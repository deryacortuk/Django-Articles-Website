from django.contrib import admin
from .models import Article,Comment
from mptt.admin import MPTTModelAdmin

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('content', 'title','author','tags')
    list_display = ['title', 'author', 'updated','publish','status','tags']
    list_display_links = ['title', 'author']
    
    class Meta:
        model = Article
        
admin.site.register(Comment, MPTTModelAdmin)
        
        
       
    
