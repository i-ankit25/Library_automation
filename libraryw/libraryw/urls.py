from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library', include('library.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url('^', include('django.contrib.auth.urls')),
]
