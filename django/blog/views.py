from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
from blog.models import *
import json

def checkAuth(request):
	if request.user.is_authenticated:
		return True
	else:
		return False

def check403(request, quser):
	if request.user.id == quser.id:
		return True
	else:
		return False

def signup(request):
    if request.method == 'POST':
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
        User.objects.create_user(username=username, password=password)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)

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
		return HttpResponse(status=405)
def signout(request):
	if request.method == 'GET':
		if checkAuth(request):
			logout(request)
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=401)      
	else:
		return HttpResponse(status=405)
#^- need config
def article(request):
	if checkAuth(request) is False: 
		return HttpResponse(status=401)
	if request.method == 'GET':
		raw = Article.objects.all()
		rst = []
		for obj in raw:
			tmpdict={}
			tmpdict['id']=obj.id
			tmpdict['title']=obj.title
			tmpdict['content']=obj.content
			tmpdict['author']=obj.author.id
			rst.append(tmpdict)
		
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
		return HttpResponse(status=405)

def article_id(request, article_id):
	#print(article_id)
	if checkAuth(request) is False: 
		return HttpResponse(status=401)
	
	art_g = Article.objects.all().filter(id=article_id)
	if art_g.count() == 0:
		return HttpResponse(status=404)
	art = Article.objects.all().filter(id=article_id)
	art=art.get()
	if request.method == 'GET':
		art = Article.objects.all().filter(id=article_id)
		art=art.get()
		tmpdict={"id":art.id,
			"title":art.title, "content":art.content,
			"author":art.author.id
		}
		return JsonResponse(tmpdict,status=200)
	
		
	elif request.method == 'PUT':
		req_data = json.loads(request.body.decode())
		title = req_data['title']
		content = req_data['content']
		art = Article.objects.filter(id=article_id).get()
		if check403(request, art.author) is False:
			return HttpResponse(status=403)
	
		art.title = title
		art.content = content
		art.save()
		return HttpResponse(status=200)
	elif request.method == 'DELETE':
		art = Article.objects.filter(id=article_id).get()
		if check403(request, art.author) is False:
			return HttpResponse(status=403)
		art.delete()
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=405)
def comment(request, article_id):
	#print(article_id)
	if checkAuth(request) is False: 
		return HttpResponse(status=401)
	
	art_g = Article.objects.all().filter(id=article_id)
	if art_g.count() == 0:
		return HttpResponse(status=404)
	
	if request.method == 'GET':
		raw = Comment.objects.filter(article_id = article_id)
		rst = []
		for obj in raw:
			tmpdict={}
			tmpdict['id']=obj.id
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
	if checkAuth(request) is False: 
		return HttpResponse(status=401)
	
	comg = Comment.objects.all().filter(id=comment_id)
	if comg.count() == 0:
		return HttpResponse(status=404)
	
	if request.method == 'GET':
		com = Comment.objects.all().filter(id=comment_id)
		com = com.get()
		tmpdict={
			"id":com.id,
			"article":com.article.id, "content":com.content,
			"author":com.author.id
		}
		return JsonResponse(tmpdict,status=200)
	elif request.method == 'PUT':
		req_data = json.loads(request.body.decode())
		content = req_data['content']
		com = Comment.objects.filter(id=comment_id).get()
	
		if check403(request, com.author) is False:
			return HttpResponse(status=403)
		
		com.content = content
		com.save()
		return HttpResponse(status=200)
	elif request.method == 'DELETE':
		com=comg.get()
		if check403(request, com.author) is False:
			return HttpResponse(status=403)
		
		com.delete()
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=405)

@ensure_csrf_cookie
def token(request):
	
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])
