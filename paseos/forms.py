from django import forms
from .models import Chiva
from .models import Paseo
from .models import Paquete

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