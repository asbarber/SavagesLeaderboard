from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *

USER_NAME_MAXLENGTH = 40
USER_PASSWORD_MAXLENGTH = 20


# HELPER
# ###############################################
def contains(list, filter):
	for x in list:
		if filter(x):
			return True
	return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# SESSIONS
# ###############################################
def delete_session_user(session):
	session.pop('user', None)

def set_session_user(session, username):
	session['user'] = username

def has_session_user(session):
	return 'user' in session

def get_session_user(session):
	return get_user(session['user'])
	
def encrypt(password):
	return password


# USERS 
# ###############################################
def get_user(username):
	return User.objects.filter(username=username)[0]

def get_users():
	return User.objects.order_by('username')

def get_ranked_users():
	users = list(get_users())
	users.sort(key=lambda x: x.calculatePoints, reverse=True)
	return users

def user_exists(username, password):
	return User.objects.filter(username=username, password=encrypt(password)).exists()

def validate_name(name):
	return len(name) > 0 and len(name) < USER_NAME_MAXLENGTH

def validate_password(password, password2):
	return password == password2 and len(password) < USER_PASSWORD_MAXLENGTH

def update_user(user, name, password):
	user.name = name
	if len(password) != 0:
		user.password = encrypt(password)
	user.save()


# ACHIEVEMENT
# ###############################################
def achievement_exists(achievementId):
	return Achievement.objects.filter(id=achievementId).exists()

def get_achievement(achievementId):
	return Achievement.objects.filter(id=achievementId)

def get_achievements():
	return Achievement.objects.all().order_by('-points')

def save_achievement(points, description):
	Achievement(points=points, description=description).save()

def remove_achievement(achievementId):
	UserAchieved.objects.filter(achievementId=achievementId).delete()
	Achievement.objects.filter(id=achievementId).delete()


# USER ACHIEVED
# ###############################################
def get_achieve_links(user):
	return UserAchieved.objects.filter(userId=user.id)

def link_exists(user, achievementId):
	return UserAchieved.objects.filter(userId=user.id, achievementId=achievementId).exists()

def get_user_unachieved(user):
	unachievement_list = []
	user_list = get_user_achieved(user)
	all_list = get_achievements()
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
