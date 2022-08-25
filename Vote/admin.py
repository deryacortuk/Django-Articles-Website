from django.contrib import admin

from Vote.models import Like,DailyLike,BrandLike


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    
    list_display = ['article', 'user', 'like',  'articlecomment']
    
    class Meta:
        model = Like
        
@admin.register(DailyLike)
class DailyAdmin(admin.ModelAdmin):
    
    list_display = [ 'user', 'like', 'dailyd',  'dailycomment' ]
    
    class Meta:
        model =DailyLike
        
@admin.register(BrandLike)
class BrandAdmin(admin.ModelAdmin):
    
    list_display = [ 'user', 'brandlike', 'like' ]
    
    class Meta:
        model =BrandLike
        
        
