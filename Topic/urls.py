from django.urls import path
from . import views

app_name = "topic"

urlpatterns = [
    path('<slug>/', views.topic,name='topic'),
]


