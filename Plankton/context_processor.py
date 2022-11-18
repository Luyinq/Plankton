from Plankton.models import Membership


def total_carrito(request):
    total = 0
    if "carrito" in request.session.keys():
        user = request.user
        sub, created=Membership.objects.get_or_create(userid=user)
        for key, value in request.session["carrito"].items():
            if sub.tipo == "donante":
                total = round(int(value["acumulado"])-(int(value["acumulado"])*0.05))
                mensaje = "Se ha aplicado el descuento de suscriptor, el total es: "
            else:
                total += int(value["acumulado"])
                mensaje = "El total es: "
    return {"total_carrito": total}