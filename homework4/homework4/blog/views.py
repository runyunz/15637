from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from blog.models import *
from blog.forms import *   

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

import hashlib, random

def index(request):
    # print request.user.is_authenticated
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        context = {'posts': Post.get_all_posts()}
        return render(request, 'blog/index.html', context)

@login_required
def home(request):
    follower = get_object_or_404(Follower, follower=request.user)
    if not follower:
        raise Http404
    posts = Post.get_posts(follower.followees.all())
    context = {'followees': follower.followees.all(), 'posts': posts}
    return render(request, 'blog/home.html', context)    

def post(request):
    # Sets up list of just the logged-in user's (request.user's) items
    context = {'name': request.user.first_name, 'posts': Post.get_posts([request.user]), 'form': PostForm()}
    return render(request, 'blog/post.html', context)

@login_required
def add_post(request):
    new_post = Post(user=request.user)
    form = PostForm(request.POST, request.FILES, instance=new_post)
    if not form.is_valid():
    	context = {"form": form}
    	return render(request, 'blog/post.html', context)
    new_post.save()

    return redirect(reverse('post'))

@login_required
def delete_post(request, id):
	post_to_delete = get_object_or_404(Post, user=request.user, id=id)
	post_to_delete.delete()
	return redirect(reverse('post'))

@login_required
def toggle_follow(request, username):
    followee = get_object_or_404(User, username=username)
    if not followee:
        raise Http404
    follower = get_object_or_404(Follower, follower=request.user)
    if not follower:
        raise Http404

    if followee in follower.followees.all():
        follower.followees.remove(followee)
    else:
        follower.followees.add(followee)        
    follower.save()
    return redirect(reverse('home'))

def get_user_posts(request, username):
    user = get_object_or_404(User, username=username)
    if not user:
        raise Http404
    context = {'posts': Post.get_posts([user]), 'followee': user}
    return render(request, 'blog/index.html', context)

def get_users(request):
    context = {'users':User.objects.all().order_by("last_name")}
    return render(request, 'blog/users.xml', context, content_type='application/xml')

def get_image(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.image:
        raise Http404
    content_type = guess_type(post.image.name)
    return HttpResponse(post.image, mimetype=content_type)

def activate(request):
	context = {}
	try:
		link_to_activate = Link.objects.get(key=request.GET['key'])
		user_to_activate = link_to_activate.user
		user_to_activate.is_active = True
		user_to_activate.save()
		context['name'] = user_to_activate.first_name
	except ObjectDoesNotExist:
		context['error'] = 'The activation key is not valid.'
	return render(request, 'blog/activation.html', context)

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'blog/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'blog/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
    									first_name=request.POST['first_name'],
    									last_name=request.POST['last_name'],
    									email=request.POST['email'],
                                        password=request.POST['password1'],
                                        )
    new_user.is_active = False
    new_user.save()

    # Creates a unique activation key for user
    new_key = generate_key(new_user.username)
    new_link = Link(key=new_key, user=new_user)
    new_link.save()

    # Send out the confirmation email
    msg = "Hi " + new_user.first_name + ", \n" + "Please use the following link to activate your account.\n" \
    	+ "http://127.0.0.1:8000/blog/activate?key=" + new_link.key + "\n"
    new_user.email_user('15637: Blog Registration Confirmation', msg, "runyunz@andrew.cmu.edu")

    # Creates a record in the follower table
    new_follower = Follower(follower=new_user)
    new_follower.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    
    if (new_user.is_active):
    	login(request, new_user)
    	return redirect(reverse('post')) #pay attention to modify here later
    else:
    	context['name'] = new_user.first_name
    	context['email'] = new_user.email
    	return render(request, 'blog/notification.html', context)

def generate_key(username):
	salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
	return hashlib.sha1(salt+username).hexdigest()

