from django.urls import path
from . import views

app_name = "follow"
urlpatterns = [
    
    path('follow/', views.follow, name= "follow" ),
    
]