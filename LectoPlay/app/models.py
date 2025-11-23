from django.db import models
import uuid

# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=120)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateField()  # Fecha seleccionada por el usuario
    creado = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre
    
class Ticket(models.Model):
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, related_name='tickets')
    estado = models.CharField(max_length=20, default='pendiente')   # pendiente / en_proceso / resuelto
    creado = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Ticket #{self.id} - {self.contacto.nombre}"


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='mensajes')
    autor = models.CharField(max_length=10)   # 'usuario' o 'admin'
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor}: {self.contenido[:20]}"