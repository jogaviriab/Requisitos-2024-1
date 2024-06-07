from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from . forms import ChivaForm
from . forms import PaseoForm

from django.contrib import messages

from .models import Administrador
from .models import Chiva
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

def crearPaseo(request):
    form = PaseoForm(request.POST)
    if form.is_valid():
        form.save()
        return messages.success(request, 'Paseo guardado con exito')
    else:
        form = PaseoForm()

    template = loader.get_template('crearPaseo.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context,request))

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
