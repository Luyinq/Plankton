from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import borrarDestacados, index, nosotros, tienda, donacion, faq, pagoexitoso, producto, contacto, tiendaofertas, registro, listaproductos, listausuarios, productoregistro, modificarproducto, eliminarproducto, tiendaplantas, tiendaherramientas, tiendaaccesorios, listausuarios, eliminarsub, subregistro, modificarsub, agregar_producto, eliminar_producto, restar_producto, limpiar_carrito, carrito, comprar


urlpatterns = [
    path('', index, name="index"),
    path('Plankton/carrito.html', carrito, name="carrito"),
    path('Plankton/nosotros.html', nosotros, name="nosotros"),
    path('Plankton/tienda.html', tienda, name="tienda"),
    path('Plankton/donacion.html', donacion, name="donacion"),
    path('Plankton/faq.html', faq, name="faq"),
    path('Plankton/pagoexitoso.html', pagoexitoso, name="pagoexitoso"),
    path('Plankton/producto.html/<id>', producto, name="producto"),
    path('Plankton/contacto.html', contacto, name="contacto"),
    path('registro/', registro, name="registro"),
    path('Plankton/listaproductos.html', listaproductos, name="listaproductos"),
    path('Plankton/listausuarios.html', listausuarios, name="listausuarios"),
    path('Plankton/productoregistro.html', productoregistro, name="productoregistro"),
    path('Plankton/subregistro.html', subregistro, name="subregistro"),
    path('Plankton/modificarproducto.html/<id>', modificarproducto, name="modificarproducto"),
    path('Plankton/modificarsub.html/<id>', modificarsub, name="modificarsub"),
    path('Plankton/eliminarproducto.html/<id>', eliminarproducto, name="eliminarproducto"),
    path('Plankton/eliminarsub.html/<id>', eliminarsub, name="eliminarsub"),
    path('Plankton/borrarDestacados.html', borrarDestacados, name="borrarDestacados"),
    path('Plankton/tiendaplantas.html', tiendaplantas, name="tiendaplantas"),
    path('Plankton/tiendaherramientas.html', tiendaherramientas, name="tiendaherramientas"),
    path('Plankton/tiendaaccesorios.html', tiendaaccesorios, name="tiendaaccesorios"),
    path('Plankton/tiendaofertas.html', tiendaofertas, name="tiendaofertas"),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    path('comprar/', comprar, name="comprar"),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

