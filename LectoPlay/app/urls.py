from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('ejercicios/encuentra/', views.encuentra, name='encuentra'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("ejercicios/lectura/", views.lectura_rapida_game, name="lectura_rapida_game"),

]