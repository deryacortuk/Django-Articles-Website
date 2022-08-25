
from django.conf.urls import handler500
from django.contrib import admin
from django.contrib.admin.sites import site
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
import notifications.urls
from django.contrib.sitemaps.views import sitemap
from Opes.sitemaps import StaticViewSitemap,ArticleSiteMap,CategorySiteMap,DailySiteMap,BrandSiteMap
from Opes.feeds import ArticleFeed,AtomSiteNewsFeed
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

from django.views.static import serve


sitemaps ={
    'article' : ArticleSiteMap,
    'Topics' : CategorySiteMap,
    'static':StaticViewSitemap,
    'brands' :BrandSiteMap, 
     'daily':DailySiteMap,
    }


urlpatterns = [
    path('/trinity/athena/', admin.site.urls),       
    path('', include('Porta.urls',namespace='porro')),
    path('',include('Populus.urls',namespace='user')),
    path('', include('Participes.urls', namespace='creo')),
    path('settings/', include('Profil.urls', namespace='profile')),
    path('topic/', include('Topic.urls', namespace='topic')),  
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    path('social-auth/',include('social_django.urls', namespace='social')),    
    path('user/', include("FollowUser.urls", namespace="follow")),
    path('like/',include("Vote.urls", namespace="like") ),
    path('brands/', include("Brand.urls",namespace="brands")),
    path('daily/', include('Daily.urls',namespace="daily")),   
     path('rss/', ArticleFeed(), name="rss"),
     path('feed/',ArticleFeed(), name="rss"),
     path('atom/',AtomSiteNewsFeed() , name="atom"), 
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),     
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),    
     path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
         ),name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_mail_sent.html'
         ),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirmation.html'
         ),name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_completed.html'
         ),name='password_reset_complete'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = 'Porta.views.handler_not_found'
handler500 = 'Porta.views.handler_server_error'
handler400 = 'Porta.views.handler_400'
handler403 = 'Porta.views.handler403'

