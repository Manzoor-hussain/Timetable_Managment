from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from superadmin.views import*
from django.views.static import serve 


urlpatterns = [
    
    path('login/', login_page, name='login'),
    path('', login_page),
    path('register/', register_page, name='register_page'),
    path('logout/', logout_page, name='logout'),
    path('admin/',  include(('superadmin.urls', 'superadmin'), namespace='superadmin')),
    path('', include(('user.urls', 'user'), namespace='user')),
   
    
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
