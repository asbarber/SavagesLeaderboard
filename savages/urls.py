from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^user/$', views.user, name='user'),
	url(r'^user/account/$', views.user_account, name='user_account')
]
