from django.contrib import admin
from .models import DailyModel,DailyComment
from mptt.admin import MPTTModelAdmin

# Register your models here.
@admin.register(DailyModel)
class DailyAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    
    class Meta:
        model = DailyModel
        
        
admin.site.register(DailyComment, MPTTModelAdmin)

