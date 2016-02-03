from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login, name='login'),
	url(r'^user/(?P<user_id>[a-zA-Z]+)/$', views.user, name='user'),
	url(r'^user/(?P<user_id>[a-zA-Z]+)/me/$', views.user_me, name='user_me')
]
