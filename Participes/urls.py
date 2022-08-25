from django.urls import path
from .views import delete_story,searchpage,user_list,daily_list, stories,user_about, ArticleWriteView, followinguser,detail_story,draft_stories,ArticleUpdateView,delete_story,addcomment,followuser


app_name = 'creo'

urlpatterns = [
   
    path('story/', ArticleWriteView.as_view(),name ="new_story"),
    path('@<username>/',stories,name= 'stories'),
    path('story/<slug>/',detail_story, name = 'detail' ),
    path('me/draft/',draft_stories, name='draft'),
    path('me/<slug>/',ArticleUpdateView.as_view(),name="update_story"),
    path('delete/<int:id>/',delete_story,name="delete_story"),
    path('add/comment/', addcomment, name = 'add_comment'),
    path('@<username>/followers/', followuser, name="followuser"),
    path('@<username>/follow/', followinguser, name='followinguser'),
    path('@<username>/about/',user_about,name ="user_about"),
    path('@<username>/lists/',user_list, name='lists'),
    path('@<username>/daily/', daily_list, name="daily_list"),
    path('search/result/',searchpage,name ="search"),   
    
  
    
               ]