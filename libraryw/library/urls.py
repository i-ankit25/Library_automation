from django.conf.urls import url
from . import views
app_name = 'library'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^user_login/issue/$', views.issue, name='issue'),
    url(r'^user_login/withdraw/$', views.withdraw, name='withdraw'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^error/$', views.error, name='error'),
    url(r'^invalid_login/$', views.invalid_login, name='invalid_login'),
    url(r'^search/$', views.search, name='search'),


]









