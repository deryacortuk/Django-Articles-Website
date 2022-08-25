from django.contrib import admin

from .models import BrandModel, BrandEntry

# Register your models here.
@admin.register(BrandModel)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand']
    class Meta :
        model = BrandModel
        
@admin.register(BrandEntry)
class BrandEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'brand' , 'created']
    
    class Meta:
        model = BrandEntry
