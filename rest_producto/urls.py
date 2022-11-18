from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_producto.views import lista_productos, detalle_producto
from rest_producto.viewsLogin import login


urlpatterns=[
    path('lista_productos', lista_productos, name='lista_productos'),
    path('detalle_producto/<id>', detalle_producto, name='detalle_producto'),
    path('login', login,name='login'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)