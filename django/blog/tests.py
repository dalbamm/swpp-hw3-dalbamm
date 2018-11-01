from django.test import TestCase, Client
from blog.models import *
import json


class BlogTestCase(TestCase):
    def setUp(self):
        u1 = User(username='chris',password='chris')
        u2 = User(username='chris2',password='chris2')
        u1.save()
        u2.save()
        
        a1 = Article(title='a1',content='a1c',author=u1)
        a2 = Article(title='a2',content='a2c',author=u2)
        a1.save()
        a2.save()
        
        c1 = Comment(article=a1,content='c1c',author=u1)
        c2 = Comment(article=a2,content='c2c',author=u2)
        c1.save()
        c2.save()
        
    def test_csrf(self):
        # By default, csrf checks are disabled in test client
        # To test csrf protection we enforce csrf checks here
        client = Client(enforce_csrf_checks=True)
        response = client.post('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 403)  # Request without csrf token returns 403 response

        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value  # Get csrf token from cookie

        response = client.post('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)  # Pass csrf protection

        response = client.get('/api/signup')
        self.assertEqual(response.status_code, 405)  # Pass csrf protection

        response = client.put('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        response = client.delete('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        #Unauthenticated cases
        response=client.post('/api/article',json.dumps({'title': 'chris', 'content': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)  # Pass csrf protection

        response=client.post('/api/article/1',json.dumps({'title': 'chris', 'content': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)  # Pass csrf protection

        response=client.post('/api/article/1/comment',json.dumps({'title': 'chris', 'content': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)  # Pass csrf protection

        response=client.post('/api/comment/1',json.dumps({'title': 'chris', 'content': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)  # Pass csrf protection


        response=client.post('/api/signin',json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 204)  # Pass csrf protection
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value  # Get csrf token from cookie

        response=client.post('/api/signin',json.dumps({'username': 'chris', 'password': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)  # Pass csrf protection

        response = client.get('/api/signin')
        self.assertEqual(response.status_code, 405)  # Pass csrf protection

        response = client.put('/api/signin', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        response = client.delete('/api/signin', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        

        #authenticated.
        response=client.post('/api/article',json.dumps({'title': 'chris', 'content': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)  # Pass csrf protection

        response = client.get('/api/article')
        self.assertEqual(response.status_code, 200)  # Pass csrf protection

        response = client.put('/api/article', json.dumps({'title': 'chris', 'content': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        response = client.delete('/api/article', 
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        

        #for article id
        response=client.post('/api/article/1',json.dumps({'title': 'chris', 'content': 'chris2'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        response = client.get('/api/article/0')
        self.assertEqual(response.status_code, 404)  # Pass csrf protection

        response = client.get('/api/article/1')
        self.assertEqual(response.status_code, 200)  # Pass csrf protection

        response = client.put('/api/article/1', json.dumps({'title': 'chris', 'content': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 403)  # Pass csrf protection
        
        response = client.delete('/api/article/1', 
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 403)  # Pass csrf protection
        
        response = client.put('/api/article/3', json.dumps({'title': 'chris', 'content': 'chris222'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)  # Pass csrf protection
        
        response = client.delete('/api/article/1', 
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)  # Pass csrf protection
        

















        response = client.post('/api/signout', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection

        response = client.get('/api/signout')
        self.assertEqual(response.status_code, 204)  # Pass csrf protection

        response = client.get('/api/signout')
        self.assertEqual(response.status_code, 401)  # Pass csrf protection

        response = client.put('/api/signout', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        response = client.delete('/api/signout', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
        
        