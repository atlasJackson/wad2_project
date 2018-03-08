from django.conf.urls import url
from fives import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),

    url(r'^match_list/$', views.match_list, name='match_list'),
    url(r'^create_match/$', views.create_match, name='create_match'),
    #url(r'^create_match/chosen_match$', views.create_match, name='chosen_match'),
    #url(r'^create_match/chosen_match/edit_match$', views.create_match, name='edit_match'),

    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
    url(r'^my_account/$', views.my_account, name='my_account'),
    #url(r'^my_account/edit_account$', views.edit_account, name='edit_account'),
    #url(r'^my_account/history$', views.history, name='history'),
    
]
