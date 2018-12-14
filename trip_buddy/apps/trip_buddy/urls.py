from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('travels', views.dashboard),
    path('view/<int:id>', views.details),
    path('addtrip',views.addtrip),
    path('newtrip', views.newtrip),
    path('join/<int:id>', views.join),
    path('cancel/<int:id>', views.cancel),
    path('delete/<int:id>', views.delete),
    path('logout', views.logout)
]