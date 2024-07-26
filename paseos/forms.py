from django import forms
from .models import Chiva, Cliente, CuentaBancaria
from .models import Paseo
from .models import Paquete
from .models import Reserva
from django.core.exceptions import ValidationError

class ConsultaReservaForm(forms.Form):
    reserva_id = forms.IntegerField(label='ID de la Reserva')

class ChivaForm(forms.ModelForm):
    class Meta:
        model = Chiva
        fields = ['placa', 'capacidad', 'tipo', 'estado']

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ['nombre', 'descripcion', 'valor']

class PaseoForm(forms.ModelForm):
    class Meta:
        model = Paseo
        fields= ['origen', 'destino', 'descripcion','fecha','disponibilidad', 'hora', 'chiva','esquemaCobro' ]

class PagarReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['comprobantePago']
        widgets = {
            'comprobantePago': forms.ClearableFileInput(attrs={'accept': 'image/jpeg'}),
        }

    def clean_comprobantePago(self):
        comprobante = self.cleaned_data.get('comprobantePago')
        if comprobante:
            if hasattr(comprobante, 'content_type'):
                if comprobante.content_type not in ['image/jpeg']:
                    raise forms.ValidationError("Solo se permiten archivos JPG.")
            else:
                raise forms.ValidationError("Error en el archivo subido.")
        return comprobante
    
class ReservaIDForm(forms.Form):
    reserva_id = forms.IntegerField(label='ID de la Reserva')

class CuentaBancariaForm(forms.ModelForm):
    class Meta:
        model = CuentaBancaria
        fields = ['numCuenta', 'tipoCuente', 'entidadBancaria']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'id', 'celular', 'correo', 'edad']
        labels = {
            'nombre': 'Nombre Completo',
            'id': 'Identificación',
            'celular': 'Celular',
            'correo': 'Correo',
            'edad': 'Edad',
        }

    def save(self, commit=True):
        cliente = super().save(commit=False)
        if commit:
            cliente.rol = 'cliente'
            cliente.save()
        return cliente


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = []