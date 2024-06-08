from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

import base64

from . forms import ChivaForm
from . forms import PaseoForm

from django.contrib import messages

from .models import Administrador
from .models import Chiva
from .models import Paseo
from .models import EsquemaCobro
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Paseos index.")

def verAdmins(request):
    listaAdmins =  Administrador.objects.all()
    template = loader.get_template('verAdmins.html')
    context = {
        'listaAdmins': listaAdmins,
    }
    return HttpResponse(template.render(context, request))

import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Chiva, EsquemaCobro, Paseo

def crearPaseo(request):
    listaChivas = Chiva.objects.all()
    if request.method == 'POST':
        print("Entra acá")
        # Al crear un paseo primero se tiene que crear el esquema de cobro
        # Creamos esquema de cobro
        esquema = request.POST.get('esquema')
        valor = request.POST.get('valor')
        equilibrio = request.POST.get('equilibrio')
        aumento = request.POST.get('aumento')
        volumen = request.POST.get('volumen')
        descuento = request.POST.get('descuento')

        if esquema == "Tipo Aerolinea":
            esquemaCobro = EsquemaCobro(tipo=esquema, fechaAumento=aumento,valorAumento=valor)
            esquemaCobro.save()
        elif esquema == "Tipo Volumen":
            esquemaCobro = EsquemaCobro(tipo=esquema, puntoEquilibrio = equilibrio, descuento=descuento)
            esquemaCobro.save()
        else:
            messages.error(request, 'Esquema de cobro no válido')
            return render(request, 'crearPaseo.html', {'listaChivas': listaChivas})

        # Creamos el paseo
        origen = request.POST.get('origen')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        destino = request.POST.get('destino')
        chiva = request.POST.get('chiva')
        descripcion = request.POST.get('descripcion')

        # Leemos contenido de la imagen
        imagen = request.FILES.get('imagen')
        if imagen:
            imagenContenido = imagen.read()
            # Convertir el contenido de la imagen a una cadena Base64
            imagen_base64 = base64.b64encode(imagenContenido).decode('utf-8')
        else:
            imagen_base64 = None

        paseo = Paseo(
            origen=origen, fecha=fecha, hora=hora, destino=destino,
            chiva=chiva, descripcion=descripcion, esquemaCobro=esquemaCobro,
            imagen=imagen_base64
        )
        paseo.save()

        messages.success(request, 'Paseo guardado con éxito')
        return redirect('./')  # Redirigir a la página adecuada después de guardar

    template = loader.get_template('crearPaseo.html')
    context = {
        'listaChivas': listaChivas,
    }
    return HttpResponse(template.render(context, request))


def chivas(request):
    if request.method == 'POST':
        form = ChivaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chiva guardada con exito')
            # return HttpResponse('Chiva guardada')
    else:
        form = ChivaForm()

    listaChivas = Chiva.objects.all()
    template = loader.get_template('chivas.html')
    context = {
        'listaChivas': listaChivas,
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def eliminarChiva(request, placa):
    try:
        chiva = Chiva.objects.get(pk=placa)
    except Chiva.DoesNotExist:
        return messages.error('Chiva no encontrada')
    
    chiva.delete()
    messages.warning(request, 'Chiva eliminada con exito')
    return redirect('../')
