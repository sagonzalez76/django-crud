from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.





# Create your models here.

# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     otp_id = models.CharField(max_length=255, blank=True, null=True)


class Document(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='documentos/')
    remitente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='documentos_enviados')
    aprobador = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='documentos_aprobados', null=True, blank=True)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo + ' - remitente ' + self.remitente.username
