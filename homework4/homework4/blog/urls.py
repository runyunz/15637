from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index', name='index'),
    url(r'^home$', 'blog.views.home', name='home'),    
    url(r'^post$', 'blog.views.post', name='post'),
    url(r'^add-post$', 'blog.views.add_post', name='add'),
    url(r'^delete-post/(?P<id>\d+)$', 'blog.views.delete_post', name='delete'),   
    url(r'^image/(?P<id>\d+)$', 'blog.views.get_image', name='image'), 
    url(r'^toggle-follow/(?P<username>\w+)$', 'blog.views.toggle_follow', name='toggle-follow'),
    url(r'^users$', 'blog.views.get_users', name='users'),
    url(r'^user-posts/(?P<username>\w+)$', 'blog.views.get_user_posts', name='user-posts'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'blog/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout',{'next_page': '/blog'}, name='logout'),
    url(r'^register$', 'blog.views.register', name='register'),
    url(r'^activate$', 'blog.views.activate', name='activate'),

)
