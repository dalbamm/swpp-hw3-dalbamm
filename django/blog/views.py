from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import ensure_csrf_cookie
from blog.models import *
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
		us = authenticate(username=str(qusername), password=str(qpassword))
		#print(us)
		if us is not None:
			login(request, us)
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=401)
	else:
		return HttpResponse(status=401)
def signout(request):
	if request.method == 'GET':
		if request.user is not None:
			logout()
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=401)      
	else:
		return HttpResponse(status=401)
#^- need config
def article(request):
	if request.method == 'GET':
		raw = Article.objects.all()
		rst = []
		for obj in raw:
			tmpdict={}
			tmpdict['title']=obj.title
			tmpdict['content']=obj.content
			tmpdict['author']=obj.author.id
			rst.append(tmpdict)
			#print(rst)
		return JsonResponse(rst,status=200,safe=False)
	elif request.method == 'POST':
		req_data = json.loads(request.body.decode())
		title = req_data['title']
		content = req_data['content']
		art = Article(title=title, content=content, author=request.user)
#create in db
		art.save()
		
		return HttpResponse(status=201)
	else:
		return HttpResponseNotAllowed(['POST'])

def article_id(request, article_id):
	#print(article_id)
	if request.method == 'GET':
		art = Article.objects.all().filter(id=article_id).get()
		if art==null:
			return HttpResponse(status=405)
		tmpdict={"title":art.title, "content":art.content,
			"author":art.author.id
		}
		print(tmpdict)
		return JsonResponse(tmpdict,status=200)
	elif request.method == 'PUT':
		req_data = json.loads(request.body.decode())
		title = req_data['title']
		content = req_data['content']
		art = Article.objects.filter(id=article_id).get()
		art.title = title
		art.content = content
		art.save()
		return HttpResponse(status=200)
	elif request.method == 'DELETE':
		req_data = json.loads(request.body.decode())
		title = req_data['title']
		content = req_data['content']
		art = Article.objects.filter(id=article_id).get()
		art.delete()
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=405)
def comment(request, article_id):
	#print(article_id)
	if request.method == 'GET':
		raw = Comment.objects.filter(article_id = article_id)
		rst = []
		for obj in raw:
			tmpdict={}
			tmpdict['article']=obj.article_id
			tmpdict['content']=obj.content
			tmpdict['author']=obj.author.id
			rst.append(tmpdict)
		return JsonResponse(rst,status=200,safe=False)
	elif request.method == 'POST':
		req_data = json.loads(request.body.decode())
		content = req_data['content']
		com = Comment(article=Article.objects.filter(id=article_id).get(), content=content, author=request.user)
		com.save()		
		return HttpResponse(status=201)
	else:
		return HttpResponse(status=405)
def comment_id(request, comment_id):
	print(comment_id)
	if request.method == 'GET':
		return null
	elif request.method == 'PUT':
		return null
	elif request.method == 'DELETE':
		return null
	else:
		return HttpResponse(status=201)

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])
'''
com = Comment.objects.all().filter(article.id=article_id).get()
		tmpdict={"title":art.title, "content":art.content,
			"author":art.author.id
		}
		print(tmpdict)
		
'''