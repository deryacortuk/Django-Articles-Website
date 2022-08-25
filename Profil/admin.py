from django.contrib import admin
from Profil.models import Profile




@admin.register(Profile)
class BrandEntryAdmin(admin.ModelAdmin):
    list_display = ['user']
    
    class Meta:
        model = Profile
