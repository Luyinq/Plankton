from django.forms import CharField
from rest_framework import serializers
from Plankton.models import Producto, Categoria, Membership
from datetime import datetime

date = datetime.today()

class ProductoSerializer(serializers.ModelSerializer):

    valoroferta = serializers.SerializerMethodField('valor_oferta')
    
    def valor_oferta(self, prod):
        return round(prod.precio - (prod.precio * (prod.descuento/100)))

    class Meta:
        model = Producto
        fields = ['idProducto', 'nombre', 'descripcion', 'precio', 'cantidad', 'descuento', 'foto', 'destacado', 'categoria', 'valoroferta']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):

    activo = serializers.SerializerMethodField('estado_sub')
    
    def estado_sub(self, sub):
        if int(sub.final.strftime('%Y%m%d')) > int(date.strftime('%Y%m%d')):
            membership=Membership.objects.get(userid=sub.userid)
            membership.tipo = "donante"
            membership.save()
            return True
        else:
            membership=Membership.objects.get(userid=sub.userid)
            membership.tipo = "free"
            membership.save()
            return False

    
    username=serializers.CharField(source="userid.username")

    class Meta:
        model = Membership
        fields = ['userid', 'username', 'tipo', 'inicio', 'final', 'activo']
    