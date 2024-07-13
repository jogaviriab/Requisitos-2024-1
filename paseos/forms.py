from django import forms
from .models import Chiva
from .models import Paseo
from .models import Paquete
from .models import Reserva
from django.core.exceptions import ValidationError


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
            'comprobantePago': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg, image/png'})
        }

    def clean_comprobantePago(self):
        comprobante = self.cleaned_data.get('comprobantePago')

        if comprobante:
            if not comprobante.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError('Solo se permiten archivos JPG y PNG.')
            #Se necesita restringir límite de espacio para db?
            if comprobante.size > 5*1024*1024:
                raise ValidationError('El tamaño del archivo no debe exceder los 5 MB.')

        return comprobante
