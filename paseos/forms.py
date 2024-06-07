from django import forms
from .models import Chiva
from .models import Paseo

class ChivaForm(forms.ModelForm):
    class Meta:
        model = Chiva
        fields = ['placa', 'capacidad', 'tipo', 'estado']

class PaseoForm(forms.ModelForm):
    class Meta:
        model = Paseo
        fields= ['origen', 'destino', 'descripcion','fecha','disponibilidad', 'hora', 'chiva','esquemaCobro' ]