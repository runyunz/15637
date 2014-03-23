from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^add-post', 'blog.views.add_post', name='add'),
    url(r'^delete-post/(?P<id>\d+)$', 'blog.views.delete_post', name='delete'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'blog/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'blog.views.register', name='register'),
    url(r'^activate$', 'blog.views.activate', name='activate'),

)
