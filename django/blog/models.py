from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField(max_length=120)
	author = models.ForeignKey(
			User,
			on_delete=models.CASCADE,
			related_name='author_set',
	)
