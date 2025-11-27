from django.urls import path
from . import views
from .views import encuentra

urlpatterns = [
    path('', views.inicio_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),

    # JUEGOS
    path('ejercicios/encuentra/', views.encuentra, name='encuentra'),
    path("ejercicios/palabras_colores/", views.palabras_colores, name="palabras_colores"),
    path("ejercicios/lectura/", views.lectura_rapida_game, name="lectura_rapida_game"),
    path("ejercicios/desc_palabra/", views.desc_palabra, name="desc_palabra"),
    path("ejercicios/pnp/", views.pnp, name="pnp"),

    # LOGIN / REGISTRO
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # CHATBOT API
    path('api/chatbot_ask', views.chatbot_ask, name='chatbot_ask'),

    # CONTACTO
    path('contacto/', views.contacto_view, name='contacto'),
    path('ticket/<str:codigo>/', views.usuario_ver_ticket, name='usuario_ver_ticket'),
    path('ticket/<int:ticket_id>/finalizar/', views.finalizar_ticket, name='finalizar_ticket'),
    path("toggle_tts/", views.toggle_tts_pc, name="toggle_tts"),

    # PANEL ADMIN
    path("panel-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("panel-admin/usuarios/", views.admin_usuarios, name="admin_usuarios"),
    path("panel-admin/usuarios/nuevo/", views.admin_usuario_nuevo, name="admin_usuario_nuevo"),
    path("panel-admin/usuarios/editar/<int:user_id>/", views.admin_usuario_editar, name="admin_usuario_editar"),
    path("panel-admin/usuarios/eliminar/<int:user_id>/", views.admin_usuario_eliminar, name="admin_usuario_eliminar"),
    path("panel-admin/consultas/", views.admin_consultas, name="admin_consultas"),
    path('panel-admin/consultas/<int:ticket_id>/', views.consulta_detalle, name='consulta_detalle'),
    path('admin/estado/<int:ticket_id>/', views.cambiar_estado, name='cambiar_estado'),
]
