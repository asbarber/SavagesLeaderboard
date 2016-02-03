from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from ..models import *
from api import *
 
def logout(request):
	if has_session_user(request.session):
		delete_session_user(request.session)
		
	return HttpResponseRedirect('/savages')
