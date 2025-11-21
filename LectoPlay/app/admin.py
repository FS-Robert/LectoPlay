from django.contrib import admin
from .models import Contacto

# Register your models here.

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'fecha_envio', 'creado')
    search_fields = ('nombre', 'correo', 'mensaje')
    list_filter = ('fecha_envio',)