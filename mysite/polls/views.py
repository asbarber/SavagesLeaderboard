from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader
from .models import *

USER_NAME_MAXLENGTH = 40
USER_PASSWORD_MAXLENGTH = 20
TEMPLATE_USER_ACHIEVE = 'polls/user.html'

# HELPER
# #############################################################################
def get_user(username):
	return User.objects.filter(username=username)[0]

def get_users():
	return User.objects.order_by('-username')

def encrypt(password):
	return password

def user_exists(username, password):
	return User.objects.filter(username=username, password=encrypt(password)).exists()

def validate_name(name):
	return len(name) > 0 and len(name) < USER_NAME_MAXLENGTH

def validate_password(password, password2):
	return password == password2 and len(password) < USER_PASSWORD_MAXLENGTH

def get_achieve_links(user):
	return UserAchieved.objects.filter(userId=user.id)

def link_exists(user, achievementId):
	return UserAchieved.objects.filter(userId=user.id, achievementId=achievementId).exists()

def achievement_exists(achievementId):
	return Achievement.objects.filter(id=achievementId).exists()

def get_achievement(achievementId):
	return Achievement.objects.filter(id=achievementId)

def get_all_achievements():
	return Achievement.objects.all()

def contains(list, filter):
	for x in list:
		if filter(x):
			return True
	return False

def get_user_unachieved(user):
	unachievement_list = []
	user_list = get_user_achieved(user)
	all_list = get_all_achievements()
	return [a for a in all_list if not contains(user_list, lambda link: link.id == a.id)]

def get_user_achieved(user):
	achievement_list = []
	for link in get_achieve_links(user):
		achievement_list += get_achievement(link.achievementId)
	return achievement_list

def save_user_achieved(user, achievementId):
	UserAchieved(userId=user.id, achievementId=achievementId).save()

def remove_user_achieved(user, achievementId):
	UserAchieved.objects.filter(userId=user.id, achievementId=achievementId).delete()



# INDEX
# #############################################################################
def index(request):
	return render(request, 'polls/index.html', {'user_list': get_users()})

# LOGIN
# #############################################################################
def login(request):
	if request.method == 'GET':
		return render(request, 'polls/login.html')
	else:
		username = request.POST['username']
		password = request.POST['password']
		if user_exists(username, password):
			return HttpResponseRedirect('/polls/user/%s' % username)
		else:
			return render(request, 'polls/login.html', {'failed': True})


# USER ME
# #############################################################################
def user_me(request, user_id):
	# Check session

	if request.method == 'GET':
		return render(request, 'polls/me.html', {'user': get_user(user_id)})
	else:
		# PARSE
		name = request.POST['name']
		password = request.POST['password']
		password2 = request.POST['password2']

		# VALIDATE
		if not validate_name(name) or not validate_password(password, password2):
			return render(request, 'polls/me.html', {'user': get_user(user_id), 'failed': True})

		# SAVES
		current = get_user(user_id)
		current.name = name
		if len(password) != 0:
			current.password = encrypt(password)
		current.save()

		# RENDER
		return render(request, 'polls/me.html', {'user': get_user(user_id)})


# USER
# #############################################################################
def user(request, user_id):
	# Check session
	user = get_user(user_id)

	if request.method == 'POST':
		achievementId = request.POST['achievementId']
		actionType = request.POST['actionType']

		if actionType == 'ADD':
			# VALIDATE
			if not achievement_exists(achievementId) or link_exists(user, achievementId):
				return render(request, TEMPLATE_USER_ACHIEVE, {'user': user, 'failed': True})

			# SAVES
			save_user_achieved(user, achievementId)
		elif actionType == 'REMOVE':
			# VALIDATE
			if not achievement_exists(achievementId):
				return render(request, TEMPLATE_USER_ACHIEVE, {'user': user, 'failed': True})

			# SAVES
			remove_user_achieved(user, achievementId)

	# RENDER
	return render(request, TEMPLATE_USER_ACHIEVE, {
		'user': user,
		'achieved': get_user_achieved(user),
		'unachieved': get_user_unachieved(user)
	})
