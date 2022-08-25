from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('me/',views.profilepage, name='me'),
    path('me/edit/',views.profileuser,name='profile_update'),
    path('addlist/<id>/',views.add_list,name="add_list"),
    path('removelist/<id>/',views.remove_list,name="remove_list"),
    path('topic/add/<id>/',views.add_topic,name="add_topic"),
    path('topic/remove/<id>/', views.remove_topic,name="remove_topic"),
    path('brand/addfollow/<id>/',views.brand_follow,name="brand_follow"),
    path('brand/removefollow/<id>/',views.remove_follow,name='remove_follow'),
  
    path('success/',views.password_success,name="passwordsuccess"),
    path('changepassword/',views.PasswordsChangeView.as_view(template_name='Profile/passwordchange.html'),name="passwordchange"),
    
]