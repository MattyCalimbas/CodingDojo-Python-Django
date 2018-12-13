from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('wall', views.wall),
    path('post_message', views.post_message),
    path('post_comment', views.post_comment),
    path('logout', views.logout)
]