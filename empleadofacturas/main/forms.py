from django import forms
from .models import Empleado, Cliente, Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        initial = {}

    def __init__(self, *args, **kwargs):       
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields["precio"].initial = 0

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        initial = {}

    def __init__(self, *args, **kwargs):       
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields["rfc"].initial = "XAXX010101000"

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = "__all__"
        initial = {
            "pago_hora" : 0,
            "pago_dia" : 0
        }

    def __init__(self, *args, **kwargs):
        # self.user = user
        # self.usergroups = Group.objects.filter(user=self.user)
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields["pago_hora"].initial = 0
        self.fields["pago_dia"].initial = 0
        # self.fields['sharegp'].queryset = self.usergroups