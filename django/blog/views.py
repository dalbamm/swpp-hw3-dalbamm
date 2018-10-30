from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import ensure_csrf_cookie
import json


def signup(request):
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
        User.objects.create_user(username=username, password=password)
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed(['POST'])

def signin(request):
	if request.method == 'POST':
		req_data = json.loads(request.body.decode())
		qusername = req_data['username']
		qpassword = req_data['password']
		print(qusername)
		print(qpassword)
		us = authenticate(username=str(qusername), password=str(qpassword))
		print(us)
		if us is not None:
			login(request, us)
			print(1)
			return HttpResponse(status=204)
		else:
			print(2)
			return HttpResponseNotAllowed(['POST'])
	else:
		print(3)
		return HttpResponseNotAllowed(['POST'])


@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])
