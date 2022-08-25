from django.urls import path
from . import views

app_name="brands" 

urlpatterns = [
    path('<slug>/', views.brandpage, name="brand"),
    path('delete/<id>/', views.delete_comment, name="comment_delete"),
   
   
  
 
    
]