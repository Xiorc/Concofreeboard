from board import views
from django.urls import path, re_path



app_name = 'board'

urlpatterns = [
    path('board/', views.index.as_view(), name='index'),
    path('board/new/', views.new_post, name='new_post'),
    re_path(r'^board/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    re_path(r'^board/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    re_path(r'^board/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    re_path(r'^board/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]