from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *
from api import *

success = False
fail = True
def create_render(request, failed):
	user = get_session_user(request.session)	
	return render(request, 'savages/create.html', {
		'user': user,
		'session': user.username,
		'achievements': get_achievements(),
		'failed': failed
	})


def create_get(request):
	return create_render(request, success)


def create_post_add(request):
	user = get_session_user(request.session)
	points = request.POST['points']
	description = request.POST['description']
	
	# valid achievement to add
	if not is_number(points):
		return create_render(request, fail)

	save_achievement(points, description)
	return create_render(request, success)

def create_post_remove(request):
	achievementId = request.POST['achievementId']
	user = get_session_user(request.session)

	# valid achievement to remove
	if not achievement_exists(achievementId):
		return create_render(request, fail)

	remove_achievement(achievementId)
	return create_render(request, success)


def create(request):
	if not has_session_user(request.session):
		return HttpResponseRedirect('/savages/login')

	if request.method == 'GET':
		return create_get(request)

	if request.method == 'POST' and request.POST['actionType'] == 'ADD':
		return create_post_add(request)

	if request.method == 'POST' and request.POST['actionType'] == 'REMOVE':
		return create_post_remove(request)