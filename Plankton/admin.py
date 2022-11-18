from django.contrib import admin
from .models import Usuario, Categoria, Producto, Membership

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Membership)