from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, Context
import sqlite3 as sql
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from Plankton.Carrito import Carrito
from Plankton.models import Producto, Membership, Categoria
from  .forms import FormDonation, ProductoRegForm, FormContacto, SubRegForm, UserCreationForm
from rest_framework import viewsets
from rest_producto.serializers import ProductoSerializer, CategoriaSerializer, MembershipSerializer
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.authtoken.models import Token
import datetime
from dateutil.relativedelta import relativedelta



# Create your views here.
def token():
    token=Token.objects.get(user=1)
    mytoken=str(token)
    return mytoken

@permission_classes((IsAdminUser,))
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication]
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.request.method in ['POST' ,'PUT', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre')
        destacado = self.request.GET.get('destacado')
        oferta = self.request.GET.get('oferta')
        categoria = self.request.GET.get('categoria')
        idProducto = self.request.GET.get('identificador')

        if nombre:
            productos = productos.filter(nombre__contains=nombre)

        elif destacado:
            productos = productos.filter(destacado=True)

        elif oferta:
            productos = productos.exclude(descuento=0)

        elif categoria:
            productos = productos.filter(categoria=categoria)

        elif idProducto:
            productos = productos.filter(idProducto=idProducto)
    
        return productos
               
@permission_classes((IsAuthenticated,))
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication]
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.request.method in ['POST' ,'PUT', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        categorias = Categoria.objects.all()
        nombre = self.request.GET.get('nombre')

        if nombre:
            categorias = categorias.filter(nombre__contains=nombre)
        
        return categorias

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


def index(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/?destacado=true', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/index.html', {'productos':response})

def nosotros(request):
    return render(request, 'Plankton/nosotros.html')

def carrito(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/carrito.html', {'productos':response})

def tienda(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/tienda.html', {'productos':response})

def donacion(request):
    user = request.user
    context = FormDonation()
    verificar = Membership.objects.filter(userid=user)
    if request.method=="POST":
        form=FormDonation(request.POST)
        if form.is_valid():
            if verificar:
                membership=Membership.objects.update(userid=user, tipo="donante", inicio=str(datetime.date.today()), final=str(datetime.date.today()+ relativedelta(months=+1)))
                return redirect(to="pagoexitoso")
            else:
                membership=Membership.objects.create(userid=user, tipo="donante", inicio=str(datetime.date.today()), final=str(datetime.date.today()+ relativedelta(months=+1)))
                return redirect(to="pagoexitoso")
    return render(request, 'Plankton/donacion.html', {'form': context})

def faq(request):
    return render(request, 'Plankton/faq.html')

def pagoexitoso(request):
    return render(request, 'Plankton/pagoexitoso.html')



def producto(request, id):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/?identificador='+str(id), headers={'Authorization': 'Token {}'.format(token())}).json()
    context = {'selectprod': response}
    return render(request, 'Plankton/producto.html', context)

def contacto(request):
    if request.method=="POST":
        form=FormContacto(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            send_mail(info['asunto'],"Nombre: " + info['nombre'] + "\nCorreo: " + info['correo'] + "\nMensaje: " + info['mensaje'],
            info.get('correo',''),['luyinnag@gmail.com'],)
            return render(request, 'Plankton/index.html')
    else:
        form=FormContacto()
    
    return render(request, 'Plankton/contacto.html', {"form":form})

def registro(request):
    context={'form':UserCreationForm}
    if request.method=='POST':
        formulario=UserCreationForm(request.POST)
        if formulario.is_valid():    
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            if user is not None:
                login(request, user)
                return redirect(to="index")
        else:
            print("Error. Ya existe")
        context['form'] = formulario
    return render(request, 'registration/registro.html', context)

@permission_required('Plankton.view_producto', login_url="../accounts/login")
def listaproductos(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/listaproductos.html', {'productos':response})

@permission_required('Plankton.view_membership', login_url="../accounts/login")
def listausuarios(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/suscripciones/', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/listausuarios.html', {'usuarios':response})


@permission_required('Plankton.add_producto', login_url="../accounts/login")
def productoregistro(request):
    context={'form':ProductoRegForm}
    if request.method=='POST':
        formulario=ProductoRegForm(request.POST, request.FILES)
        if formulario.is_valid():    
            formulario.save()
            return redirect(to='listaproductos')
    return render(request, 'Plankton/productoregistro.html', context)

@permission_required('Plankton.add_membership', login_url="../accounts/login")
def subregistro(request):
    context={'form':SubRegForm}
    if request.method=='POST':
        formulario=SubRegForm(request.POST)
        if formulario.is_valid():    
            formulario.save()
            return redirect(to='listausuarios')
    return render(request, 'Plankton/subregistro.html', context)

@permission_required('Plankton.change_producto', login_url="../accounts/login")
def modificarproducto(request, id):
    producto=Producto.objects.get(idProducto=id)
    contexto={
        'form':ProductoRegForm(instance=producto)
    }
    if request.method=='POST':
        formulario=ProductoRegForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():    
            formulario.save()
            return redirect(to='listaproductos')
        
    return render(request, 'Plankton/modificarproducto.html', contexto)

@permission_required('Plankton.change_membership', login_url="../accounts/login")
def modificarsub(request, id):
    sub=Membership.objects.get(userid=id)
    contexto={
        'form':SubRegForm(instance=sub)
    }
    if request.method=='POST':
        formulario=SubRegForm(request.POST, instance=sub)
        if formulario.is_valid():    
            formulario.save()
            return redirect(to='listausuarios')
        
    return render(request, 'Plankton/modificarsub.html', contexto)

@permission_required('Plankton.delete_producto', login_url="../accounts/login")
def eliminarproducto(request, id):
    producto=Producto.objects.get(idProducto=id)
    producto.delete()
    return redirect(request.META['HTTP_REFERER'])

@permission_required('Plankton.delete_membership', login_url="../accounts/login")
def eliminarsub(request, id):
    sub=Membership.objects.get(userid=id)
    sub.delete()
    return redirect(request.META['HTTP_REFERER'])

def borrarDestacados(request):
    productolista=Producto.objects.filter(destacado=True)
    for producto in productolista:
        producto.destacado = False
        producto.save()
    return redirect(request.META['HTTP_REFERER'])

def tiendaplantas(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/?categoria=1', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/tiendaplantas.html', {'productos':response})

def tiendaherramientas(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/?categoria=2', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/tiendaherramientas.html', {'productos':response})

def tiendaaccesorios(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/?categoria=3', headers={'Authorization': 'Token {}'.format(token())}).json()
    return render(request, 'Plankton/tiendaaccesorios.html', {'productos':response})

def tiendaofertas(request):
    response=requests.get('http://127.0.0.1:8000/api/v2/productos/?oferta=0', headers={'Authorization': 'Token {}'.format(token())}).json()   
    return render(request, 'Plankton/tiendaofertas.html', {'productos':response})

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.agregar(producto)
    return redirect('carrito')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.eliminar(producto)
    return redirect('carrito')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.restar(producto)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('carrito')


def comprar(request):
    carrito = Carrito(request)
    carrito.comprar()
    return redirect('pagoexitoso')