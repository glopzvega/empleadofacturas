from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=255)    

# Create your models here.
class Empleado(models.Model):
    TIPO_EMPLEADO = [
        ("salario", "Asalariado"),
        ("horas", "Por Hora"),
    ]
    # empleado = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nss = models.CharField(max_length=255)    
    nombre = models.CharField(max_length=255)     
    tipo = models.CharField(max_length=255, choices=TIPO_EMPLEADO)
    pago_hora = models.FloatField()
    pago_dia = models.FloatField()    

class Nomina(models.Model):
    TIPO_EMPLEADO = [
        ("salario", "Asalariado"),
        ("horas", "Por Hora"),
    ]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    horas_trabajadas = models.FloatField(default=0)
    dias_trabajados = models.FloatField(default=0)
    monto_pago = models.FloatField(default=0)
    tipo = models.CharField(max_length=255, choices=TIPO_EMPLEADO)


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    clave = models.CharField(max_length=255)
    precio = models.FloatField()

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    # cliente = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)    
    rfc = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    folio = models.CharField(max_length=255)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.FloatField()

    def __str__(self):
        return self.folio

class LineaFactura(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    preciounitario = models.FloatField()
    descuento = models.FloatField()
    impuesto = models.FloatField()
    subtotal = models.FloatField()
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.id, self.producto.nombre)
