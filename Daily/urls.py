from django.contrib.auth import views
from django.urls import path
from .views import dailycomment, deletecomment,dailystatus,delete_comment,comment_added


app_name = "daily"

urlpatterns = [
    path('status/', dailycomment, name= "daily"),
    path('delete/<id>/', deletecomment, name="delete_daily"),
    path('addcomment/',comment_added, name="add_comment"),
    path('deletecomment/<id>/',delete_comment,name="delete_comment"),
    
    path('status/<id>/', dailystatus,name="status"),
    
]