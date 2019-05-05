from django.contrib import admin
from .models import Persona, Empleado, Cliente, Nomina, Producto, Factura, LineaFactura
# Register your models here.
# @admin.register(Persona)
# class AdminPersona(admin.ModelAdmin):
#     search_fields = ('nombre', )
#     list_display = ('id', 'nombre')

@admin.register(Empleado)
class AdminEmpleado(admin.ModelAdmin):
    search_fields = ('nombre', 'tipo')
    list_display = ('id', 'nombre', 'tipo', 'pago_hora', 'pago_dia')

@admin.register(Nomina)
class AdminNomina(admin.ModelAdmin):
    search_fields = ('empleado__nombre', )
    list_display = ('id', 'empleado', 'horas_trabajadas', 'dias_trabajados','monto_pago')

@admin.register(Cliente)
class AdminCliente(admin.ModelAdmin):
    search_fields = ('nombre', 'rfc')
    list_display = ('id', 'nombre', 'rfc')

@admin.register(Producto)
class AdminProducto(admin.ModelAdmin):
    search_fields = ('nombre', 'clave')
    list_display = ('id', 'clave', 'nombre', 'precio')

@admin.register(Factura)
class AdminFactura(admin.ModelAdmin):
    search_fields = ('cliente__nombre', 'folio', 'fecha')
    list_display = ('id', 'cliente', 'fecha', 'folio','total')

@admin.register(LineaFactura)
class AdminLineaFactura(admin.ModelAdmin):
    search_fields = ('factura_cliente__nombre', 'factura_folio', 'factura_fecha', 'producto_nombre')
    list_display = ('id', 'factura', 'producto', 'cantidad', 'preciounitario', 'descuento', 'impuesto', 'subtotal')
