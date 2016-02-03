from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *
from api import *

success = False
fail = True
def user_account_render(request, failed):
	user = get_session_user(request.session)		
	return render(request, 'savages/user_account.html', {
		'user': user,
		'session': user.username,
		'failed': failed
	})


def user_account_get(request):
	return user_account_render(request, success)


def user_account_post(request):
	name = request.POST['name']
	password = request.POST['password']
	password2 = request.POST['password2']

	# valid name and password/confirm-password
	if not validate_name(name) or not validate_password(password, password2):
		return user_account_render(request, fail)

	update_user(user, name, password)
	return user_render(request, success)


def user_account(request):
	if not has_session_user(request.session):
		return HttpResponseRedirect('/savages/login')

	if request.method == 'GET':
		return user_account_get(request)	

	if request.method == 'POST':
		return user_account_post(request)