from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('encuentra/', views.encuentra, name='encuentra'),
    path('contacts/', views.contacts, name='contacts'),
]