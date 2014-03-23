from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    def __unicode__(self):
	return self.text

class Link(models.Model):
	key = models.CharField(max_length=40)
	user = models.ForeignKey(User)
	def __unicode__(self):
		return self.key

class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100, default="", blank=True)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	
	@staticmethod
	def get_posts(user):
		return Post.objects.filter(user=user).order_by("created").reverse()

	def __unicode__(self):
		return self.title

