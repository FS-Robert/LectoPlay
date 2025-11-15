from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('ejercicios/encuentra/', views.encuentra, name='encuentra'),
   path("palabras_colores/", views.palabras_colores, name="palabras_colores"),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
<<<<<<< HEAD
    path("ejercicios/lectura/", views.lectura_rapida_game, name="lectura_rapida_game"),
=======
<<<<<<< HEAD
    
=======
>>>>>>> 7dadc2cd959caebd468b97c980cf49954a6b059a

>>>>>>> b6070dd7fc3f6693eb873477211d8ebf63f7d4b2
]