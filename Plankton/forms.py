from dataclasses import fields
from django import forms
from django.forms import widgets
from django.forms import ModelForm
from .models import Usuario, Producto, Membership
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UsuarioRegForm(ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Usuario
        fields = ['run', 'correo', 'contrasena', 'nombre', 'apaterno', 'amaterno', 'celular']


class ProductoRegForm(ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad', 'descuento', 'foto', 'destacado', 'categoria']

class SubRegForm(ModelForm):
    class Meta:
        model = Membership
        fields = '__all__'
    

class FormContacto(forms.Form):
    nombre=forms.CharField()
    asunto=forms.CharField()
    correo=forms.EmailField()
    mensaje=forms.CharField(widget=forms.Textarea)

class FormDonation(forms.Form):
    nombre=forms.CharField()
    apellido=forms.CharField()
    correo=forms.EmailField()
    celular=forms.IntegerField()
    calle=forms.CharField()
    monto=forms.IntegerField()





class CustomCreationForm(UserCreationForm):
    pass

