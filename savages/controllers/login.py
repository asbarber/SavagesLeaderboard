from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *
from api import *

def login_get(request):
	return render(request, 'savages/login.html')

# Performs log in action
def login_post(request):
	username = request.POST['username']
	password = request.POST['password']

	# invalid login
	if not user_exists(username, password):
		return render(request, 'savages/login.html', {'failed': True})

	set_session_user(request.session, username)
	return HttpResponseRedirect('/savages/user')

	
def login(request):
	# user already logged in
	if has_session_user(request.session):
		return HttpResponseRedirect('/savages')

	if request.method == 'GET':
		return login_get(request)
	
	if request.method == 'POST':
		return login_post(request)

