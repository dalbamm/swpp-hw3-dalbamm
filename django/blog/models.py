from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField(max_length=500)
	author = models.ForeignKey(
			User,
			on_delete=models.CASCADE,
			related_name='author_set',
	)
	def __str__(self):
		return "title: {}/ content: {}".format(self.title, self.content)

class Comment(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete=models.CASCADE,
		related_name='article_set'
	)
	content = models.TextField(max_length=500)
	author = models.ForeignKey(
			User,
			on_delete=models.CASCADE,
			related_name='comment_author_set',
	)
	def __str__(self):
		return "content: {}".format(self.content)