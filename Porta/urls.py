from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
app_name = 'porro'

urlpatterns = [
    path('', views.index, name = "gateway"),
    path('topics/',cache_page(60) (views.topics), name ="topics"),
    path('brands/',views.brands, name='brands'),
    path('about/',views.ourstory, name="about"),
    path('connect/', views.write,name="share"),
    path('contact/',views.contact,name="contact"),

 
  
]

