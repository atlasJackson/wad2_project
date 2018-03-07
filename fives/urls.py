from django.conf.urls import url
from fives import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^match_list/$', views.match_list, name='match_list'),
    url(r'^create_match/$', views.create_match, name='create_match'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^login/$', views.login, name='login'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),

]
