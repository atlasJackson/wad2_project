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
    url(r'^game_list/(?P<game_custom_slug>[\w\d\-]+\-\d{8}\-\d{4}\b)/leave_game/$', views.leave_game, name='leave_game'),
    url(r'^game_list/(?P<game_custom_slug>[\w\d\-]+\-\d{8}\-\d{4}\b)/delete_game/$', views.delete_game, name='delete_game'),

    url(r'^create_game/$', views.create_game, name='create_game'),

    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^user/(?P<player>[\w\d\-]+\b)/$', views.user_account, name='user_account'),
    #url(r'^user/(?P<player>[\w\d\-]+\b)/edit_account/$', views.user_account, name='edit_account'),
    url(r'^user/(?P<player>[\w\d\-]+\b)/history/$', views.history, name='history'),
    url(r'^user/(?P<player>[\w\d\-]+\b)/(?P<game_custom_slug>[\w\d\-]+\-\d{8}\-\d{4}\b)/$', views.show_past_game, name='show_past_game'),
]
