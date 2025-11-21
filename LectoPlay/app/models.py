from django.db import models

# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=120)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateField()  # Fecha seleccionada por el usuario
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo} - {self.fecha_envio}"