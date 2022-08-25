from django.urls import path
from . import views
app_name = 'user'

urlpatterns = [
    path('signup/',views.signup, name="signup"),
    path('login/', views.signin,name="login"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout_user, name='logout')
    
               ]