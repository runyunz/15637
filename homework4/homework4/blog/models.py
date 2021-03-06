from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    def __unicode__(self):
	return self.text

class Follower(models.Model):
	follower = models.ForeignKey(User, related_name='follower')
	followees = models.ManyToManyField(User, related_name='followees')
	def __unicode__(self):
		return unicode(self.follower.username)

class Link(models.Model):
	key = models.CharField(max_length=40)
	user = models.ForeignKey(User)
	def __unicode__(self):
		return self.key

class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(upload_to="blog-photos", blank=True)
	created = models.DateTimeField(auto_now_add=True)

	
	@staticmethod
	def get_posts(users):
		return Post.objects.filter(user__in=users).order_by("created").reverse()
		# return Post.objects.filter(user=user).order_by("created").reverse()

	@staticmethod
	def get_all_posts():
		return Post.objects.all().order_by("created").reverse()

	def __unicode__(self):
		return self.title

