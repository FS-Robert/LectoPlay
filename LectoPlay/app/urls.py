from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('ejercicios/encuentra/', views.encuentra, name='encuentra'),
    path("ejercicios/palabras_colores/", views.palabras_colores, name="palabras_colores"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("ejercicios/lectura/", views.lectura_rapida_game, name="lectura_rapida_game"),
    path('api/chatbot_ask', views.chatbot_ask, name='chatbot_ask'),
    path("ejercicios/desc_palabra/", views.desc_palabra, name="desc_palabra"),
    path("ejercicios/pnp/", views.pnp, name="pnp"),
    path('contacto/', views.contacto_view, name='contacto'),
    
]