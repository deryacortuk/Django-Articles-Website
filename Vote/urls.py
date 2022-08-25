from django.urls import path
from .views import likeArticle, likeDaily,articlecommentlike,dailycommentlike,brandcommentlike

app_name = "like"

urlpatterns = [
    
    path('<id>/', likeArticle, name="like"),
    path('story/<id>/', articlecommentlike, name="articlelike"),
    path('daily/<id>/daily/',likeDaily,name='daily_like'),
    path('daily/<id>/like/', dailycommentlike, name="comment_like"),
    path('brandcommentlike/<id>/', brandcommentlike, name='brand_like')
   
  
 
    
]