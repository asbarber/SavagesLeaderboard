from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.template import loader
from .models import *

from controllers.home import *
from controllers.login import *
from controllers.logout import *
from controllers.user import *
from controllers.user_account import *
from controllers.create import *