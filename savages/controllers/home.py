from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *
from api import *

def home(request):
	context = {'user_list': get_users()}

	if has_session_user(request.session):
		context['session'] = get_session_user(request.session)

	return render(request, 'savages/home.html', context)
