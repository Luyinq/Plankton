from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
# Create your models here.

#Modelo Usuarios
class Usuario(models.Model):
    run=models.IntegerField(primary_key=True, verbose_name="Rut")
    correo=models.CharField(max_length=50, verbose_name="Correo")
    contrasena=models.CharField(max_length=20, verbose_name="Contraseña")
    nombre=models.CharField(max_length=20, verbose_name="Nombre")
    apaterno=models.CharField(max_length=20, verbose_name="Apellido paterno")
    amaterno=models.CharField(max_length=20, verbose_name="Apellido materno")
    celular=models.IntegerField(verbose_name="Celular")

    def __str__(self):
        return self.run

class Categoria(models.Model):
    idCategoria=models.AutoField(primary_key=True, verbose_name="ID Categoria")
    nombreCategoria=models.CharField(max_length=50,verbose_name="Nombre Categoria")

    def __str__(self):
        return self.nombreCategoria

class Producto(models.Model):
    idProducto=models.AutoField(primary_key=True,verbose_name="ID Producto")
    nombre=models.CharField(max_length=20,verbose_name="Nombre")
    descripcion=models.CharField(max_length=200, verbose_name="Descripción")
    precio=models.IntegerField(verbose_name="Precio")
    cantidad=models.IntegerField(verbose_name="Cantidad", default=0)
    descuento=models.IntegerField(verbose_name="Porcentaje de oferta", default=0)
    foto=models.ImageField(upload_to='users/%Y/%m/%d/', height_field=None, width_field=None, max_length=100, verbose_name="Foto")
    destacado=models.BooleanField(verbose_name="Producto destacado")
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class User(models.Model):
    def __str__(self):
        return self.username


class Membership(models.Model):
    TYPE_CHOICES = (('free','Free'), ('donante','Donante'))

    userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, unique=False)
    tipo = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Tipo suscripción")
    inicio = models.DateField(default=datetime.date.today, verbose_name="Inicio suscripción")
    final = models.DateField(default=datetime.date.today, verbose_name="Final suscripción")

    def __str__(self):
        return self.userid.username

    

