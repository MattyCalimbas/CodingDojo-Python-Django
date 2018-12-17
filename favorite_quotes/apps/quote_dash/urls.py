from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('post_quote', views.post_quote),
    path('quotes', views.dashboard),
    path('user/<int:id>', views.userdetails),
    path('myaccount/<int:id>', views.editaccount),
    path('edituser', views.edituser),
    path('delete/<int:id>', views.delete),
    path('logout', views.logout)
]