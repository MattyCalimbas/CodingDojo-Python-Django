from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('amadon/buy', views.buy),
    path('checkout', views.checkout)
]