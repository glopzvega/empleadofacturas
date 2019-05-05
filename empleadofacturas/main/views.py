from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Cliente, Producto, Factura, LineaFactura, Nomina
from .forms import EmpleadoForm, ClienteForm, ProductoForm
from datetime import datetime
import json
# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def empleado_editar(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save()
            return redirect("empleados")
    else:
        form = EmpleadoForm(instance=empleado)       
    
    data = {
        "form" : form
    }
    
    return render(request, "main/empleado.html", data)

def empleado_nuevo(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save()
        return redirect("empleados")
    else:
        form = EmpleadoForm()
    
    data = {
        "form" : form
    }
    return render(request, "main/empleado.html", data)

def empleados(request):
    empleados = Empleado.objects.all()
    data = {
        "empleados" : empleados
    }
    return render(request, 'main/empleados.html', data)

def cliente_editar(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            return redirect("clientes")
    else:
        form = ClienteForm(instance=cliente)       
    
    data = {
        "form" : form
    }
    
    return render(request, "main/cliente.html", data)

def cliente_nuevo(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
        return redirect("clientes")
    else:
        form = ClienteForm()
    
    data = {
        "form" : form
    }
    return render(request, "main/cliente.html", data)

def clientes(request):
    clientes = Cliente.objects.all()
    data = {
        "clientes" : clientes
    }
    return render(request, 'main/clientes.html', data)

def producto_editar(request, id):
    producto = get_object_or_404(Producto, pk=id)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            return redirect("productos")
    else:
        form = ProductoForm(instance=producto)       
    
    data = {
        "form" : form
    }
    
    return render(request, "main/producto.html", data)

def producto_nuevo(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
        return redirect("productos")
    else:
        form = ProductoForm()
    
    data = {
        "form" : form
    }
    return render(request, "main/producto.html", data)

def productos(request):
    productos = Producto.objects.all()
    data = {
        "productos" : productos
    }
    return render(request, 'main/productos.html', data)

def _get_productos(request):
    productos = Producto.objects.all()
    productos_data = []
    for p in productos:
        productos_data.append({
            "id" : p.id,
            "nombre" : p.nombre,
            "clave" : p.clave,
            "precio" : p.precio
        })

    return JsonResponse({"success" : True, "data" : productos_data})

def _actualizar_subtotal(linea):
    monto = linea.preciounitario * linea.cantidad
    descuento = monto * (linea.descuento / 100)
    base = monto - descuento
    impuesto = base * (linea.impuesto / 100)
    subtotal = base + impuesto
    linea.subtotal = subtotal
    linea.save()
    return linea.subtotal

def factura_nueva(request):
    if request.method == "POST":
        print("#####DATA#####")
        data = json.loads(request.POST["data"])
        # print(data)        
        facturas = Factura.objects.all()
        if facturas:
            facturas = facturas.order_by("-folio")[:1]
            folio = int(facturas[0].folio) + 1 
        else:
            folio = 1
        
        if "cliente" in data and "fecha" in data:
            cliente_id = data["cliente"]
            cliente = get_object_or_404(Cliente, pk=cliente_id)
            factura = Factura(folio=folio, cliente=cliente, fecha=data["fecha"], total=0)
            factura.save()

            if factura:
                lineas = data["lineas"]  
                total = 0              
                for linea in lineas:
                    producto_id = linea["producto"]
                    producto = get_object_or_404(Producto, pk=producto_id)
                    linea_nueva = LineaFactura(producto=producto, cantidad=linea["cantidad"], preciounitario=linea["precio"], impuesto=linea["impuesto"], descuento=linea["descuento"], subtotal=0, factura=factura)
                    if linea_nueva:
                        total += _actualizar_subtotal(linea_nueva)
                    print(linea)
                factura.total = total
                factura.save()

                return JsonResponse({"success" : True, "id" : factura.id})

        return JsonResponse({"success" : False})
    else:
        clientes = Cliente.objects.all()
        clientes_data = []
        for c in clientes:
            clientes_data.append({
                "id" : c.id,
                "nombre" : c.nombre,
                "rfc" : c.rfc
            })
        
        data = {
            "clientes" : clientes_data,
            "fecha" : datetime.now().strftime("%Y-%m-%d")
        }
        return render(request, "main/factura.html", data)

def nomina_nueva(request):
    if request.method == "POST":
        data = json.loads(request.POST["data"])
        # print(data)        
                
        if "empleado" in data and "tipo" in data:
            empleado_id = data["empleado"]
            empleado = get_object_or_404(Empleado, pk=empleado_id)
            tipo = data["tipo"]            
            nomina = Nomina(empleado=empleado, tipo=tipo)
            nomina.save()

            if nomina:                
                dias = 0
                horas = 0
                total = 0
                if tipo == "salario":
                    pago = empleado.pago_dia
                    if "dias_trabajados" in data and float(data["dias_trabajados"]) > 0:
                        dias = float(data["dias_trabajados"])
                        total = pago * dias
                else:
                    pago = empleado.pago_hora                
                    if "horas_trabajadas" in data and float(data["horas_trabajadas"]) > 0:
                        horas = float(data["horas_trabajadas"])
                        total = pago * horas

                nomina.horas_trabajadas = horas                
                nomina.dias_trabajados = dias
                nomina.monto_pago = total
                nomina.save()
            
                return JsonResponse({"success" : True, "id" : nomina.id})

        return JsonResponse({"success" : False})
    else:
        empleados = Empleado.objects.all()
        data = {
            "empleados" : empleados
        }
        return render(request, "main/nomina.html", data)

def get_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    data = {
        "id" : empleado.id,
        "nombre" : empleado.nombre,
        "nss" : empleado.nss,
        "tipo" : empleado.tipo,
        "pago_hora" : empleado.pago_hora,
        "pago_dia" : empleado.pago_dia
    }
    return JsonResponse({"success" : True, "data" : data})

def facturas(request):
    data = {
        "facturas" : Factura.objects.all().order_by("-folio")
    }
    return render(request, "main/facturas.html", data)

def nominas(request):
    data = {
        "nominas" : Nomina.objects.all()
    }
    return render(request, "main/nominas.html", data)

def _get_datos_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)
    lineas = LineaFactura.objects.filter(factura=factura)
    data = {
        "factura" : {
            "cliente" : {
                "id" : factura.cliente.id,
                "nombre" : factura.cliente.nombre,
                "rfc" : factura.cliente.rfc
            },
            "fecha" : factura.fecha,
            "total" : factura.total,
            "lineas" : []
        }
    }
    if lineas:
        lineas_data = []
        for linea in lineas:
            lineas_data.append({
                "producto" : {
                    "id" : linea.producto.id,
                    "clave" : linea.producto.clave,
                    "nombre" : linea.producto.nombre,
                    "precio" : linea.producto.precio,
                },
                "cantidad" : linea.cantidad,
                "preciounitario" : linea.preciounitario,
                "impuesto" : linea.impuesto,
                "descuento" : linea.descuento,
                "subtotal" : linea.subtotal
            })
        data["factura"].update({"lineas" : lineas_data})
    return JsonResponse({"success" : True, "data" : data})

def factura_editar(request, id):
       
    if request.method == "POST":
        factura = get_object_or_404(Factura, pk=id)
        data = json.loads(request.POST["data"])
        print(data)   
        if "cliente" in data and "fecha" in data:
            cliente_id = data["cliente"]
            cliente = get_object_or_404(Cliente, pk=cliente_id)
            factura.cliente = cliente
            factura.fecha = data["fecha"]            
            factura.save()

            lineas_ant = LineaFactura.objects.filter(factura=factura)
            lineas_ant.delete()

            if factura:
                lineas = data["lineas"]  
                total = 0              
                for linea in lineas:
                    producto_id = linea["producto"]
                    producto = get_object_or_404(Producto, pk=producto_id)
                    linea_nueva = LineaFactura(producto=producto, cantidad=linea["cantidad"], preciounitario=linea["precio"], impuesto=linea["impuesto"], descuento=linea["descuento"], subtotal=0, factura=factura)
                    if linea_nueva:
                        total += _actualizar_subtotal(linea_nueva)
                    print(linea)
                factura.total = total
                factura.save()

                return JsonResponse({"success" : True, "id" : factura.id})

        return JsonResponse({"success" : False})
    else:
        factura = get_object_or_404(Factura, pk=id)
        factura.lineas = LineaFactura.objects.filter(factura=factura)
        clientes = Cliente.objects.all()
        clientes_data = []
        for c in clientes:
            clientes_data.append({
                "id" : c.id,
                "nombre" : c.nombre,
                "rfc" : c.rfc
            })

        productos = Producto.objects.all()
        productos_data = []
        for p in productos:
            productos_data.append({
                "id" : p.id,
                "nombre" : p.nombre,
                "clave" : p.clave,
                "precio" : p.precio
            })
        data = {
            "clientes" : clientes_data,
            "productos" : productos_data,
            "fecha" : factura.fecha.strftime("%Y-%m-%d"),
            "factura" : factura
        }
        return render(request, "main/factura_editar.html", data)