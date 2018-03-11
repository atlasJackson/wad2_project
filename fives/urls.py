from django.conf.urls import url
from fives import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),

    url(r'^game_list/$', views.game_list, name='game_list'),
    # regex: [\w\d]+\-\d{8}\-\d{4}\b
    # regex: \w+ = any number of characters, \- = a dash, \d{8} = eight digits, \b = a word boundary
    url(r'^game_list/(?P<game_custom_slug>[\w\d\-]+\-\d{8}\-\d{4}\b)/$', views.show_game, name='show_game'),
    url(r'^game_list/(?P<game_custom_slug>[\w\d\-]+\-\d{8}\-\d{4}\b)/join_game/$', views.join_game, name='join_game'),

    url(r'^create_game/$', views.create_game, name='create_game'),
    #url(r'^create_game/chosen_game$', views.create_game, name='chosen_game'),
    #url(r'^create_game/chosen_game/edit_game$', views.create_game, name='edit_game'),
    

    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^my_account/$', views.my_account, name='my_account'),
    #url(r'^my_account/edit_account$', views.edit_account, name='edit_account'),
    #url(r'^my_account/history$', views.history, name='history'),
]
