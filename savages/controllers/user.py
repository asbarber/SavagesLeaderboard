from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *
from api import *

success = False
fail = True
def user_render(request, failed):
	user = get_session_user(request.session)	
	return render(request, 'savages/user.html', {
		'user': user,
		'session': user.username,
		'achieved': get_user_achieved(user),
		'unachieved': get_user_unachieved(user),
		'failed': failed
	})


def user_get(request):
	return user_render(request, success)


def user_post_add(request):
	achievementId = request.POST['achievementId']
	user = get_session_user(request.session)

	# valid achievement to add
	if not achievement_exists(achievementId) or link_exists(user, achievementId):
		return user_render(request, fail)

	save_user_achieved(user, achievementId)
	return user_render(request, success)

def user_post_remove(request):
	achievementId = request.POST['achievementId']
	user = get_session_user(request.session)

	# valid achievement to remove
	if not achievement_exists(achievementId):
		return user_render(request, fail)

	remove_user_achieved(user, achievementId)
	return user_render(request, success)


def user(request):
	if not has_session_user(request.session):
		return HttpResponseRedirect('/savages/login')

	if request.method == 'GET':
		return user_get(request)

	if request.method == 'POST' and request.POST['actionType'] == 'ADD':
		return user_post_add(request)

	if request.method == 'POST' and request.POST['actionType'] == 'REMOVE':
		return user_post_remove(request)