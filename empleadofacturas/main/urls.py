from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('empleados/', views.empleados, name="empleados"),
    path('empleado/<int:id>/', views.empleado_editar, name="empleado_editar"),
    path('empleado/', views.empleado_nuevo, name="empleado_nuevo"),
    
    path('clientes/', views.clientes, name="clientes"),
    path('cliente/<int:id>/', views.cliente_editar, name="cliente_editar"),
    path('cliente/', views.cliente_nuevo, name="cliente_nuevo"),

    path('productos/', views.productos, name="productos"),
    path('producto/<int:id>/', views.producto_editar, name="producto_editar"),
    path('producto/', views.producto_nuevo, name="producto_nuevo"),

    path('facturas/', views.facturas, name="facturas"),
    path('nominas/', views.nominas, name="nominas"),
    path('factura/', views.factura_nueva, name="factura_nueva"),
    path('nomina/', views.nomina_nueva, name="nomina_nueva"),
    path('nomina/empleado/<int:id>/', views.get_empleado, name="get_empleado"),
    path('factura/<int:id>/', views.factura_editar, name="factura_editar"),
    path('factura/productos/', views._get_productos, name="factura_productos"),
    path('factura/datos/<int:id>/', views._get_datos_factura, name="factura_datos"),
]