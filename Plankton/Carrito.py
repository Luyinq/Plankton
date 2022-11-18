from .models import Producto

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        id = str(producto.idProducto)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id": producto.idProducto,
                "nombre": producto.nombre,
                "acumulado": round(producto.precio - (producto.precio * (producto.descuento/100))),
                "cantidad": 1,
            }

        else:
            if self.carrito[id]["cantidad"] < producto.cantidad:
                self.carrito[id]["cantidad"] += 1
                self.carrito[id]["acumulado"] += round(producto.precio - (producto.precio * (producto.descuento/100)))
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.idProducto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.idProducto)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= round(producto.precio - (producto.precio * (producto.descuento/100)))
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True


    def comprar(request):
        producto = Producto.objects.filter()
        for keys, value in request.session["carrito"].items():
            for y in producto:
                    if "carrito" in request.session.keys():
                        if int(value["producto_id"]) == y.idProducto:
                            print(keys[0])
                            print("borrado")
                            print(int(value["cantidad"]))
                            y.cantidad = y.cantidad - int(value["cantidad"])
                            y.save()
