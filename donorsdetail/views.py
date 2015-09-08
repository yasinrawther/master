# Create your views here.
import sys
from django.shortcuts import render
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# @login_required
def userlogin(request):
	# logout(request)
	return render(request,'userlogin.html')

@login_required
def donor(request):
	return render(request,'donor.html')


def userregister(request):
	return render(request,'userregister.html')


@login_required
def adminpage(request):
	return render(request,'adminpage.html')

@login_required
def settings(request):
	return render(request,'settings.html')


def forgetpaswd(request):
	return render(request,'forgetpaswd.html')

# @login_required
def logout_view(request):
	print 'jsdhjshdjshjd'
	logout(request)
	return HttpResponseRedirect('/userlogin/')
	# return render(request,'userlogin.html')

@login_required
def accountsetting(request):
	return render(request,'accountsetting.html')
