from django.http import HttpResponse
from django.shortcuts import redirect, render
from paseos.backends import AdminAuthentication
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from datetime import datetime, timedelta

import base64


from . forms import ChivaForm
from . forms import PaseoForm


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

def inicioSesionAdmin(request):
    if request.method == 'POST':
        email = request.POST.get('email'); email = email.lower()
        password = request.POST.get('password')
        authBack = AdminAuthentication()

        user = authBack.authenticate(request, email=email, password=password)

        if user is not None:
            return redirect('verPaseosAdmin')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    
    return render(request, 'inicioSesionAdmin.html')

def registrarPaseo(request):

    listaChivas = Chiva.objects.filter(estado='Disponible')

    # Cuando se envia los datos del formulario
    if request.method == 'POST':

        # Conseguimos la chiva con la placa y comprobamos que exista
        placaChiva = request.POST.get('chiva')
        try:
            chiva = Chiva.objects.get(placa=placaChiva)
        except ObjectDoesNotExist:
            messages.error(request,"Por favor seleccione una chiva válida.")
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})

        # Algunos datos del paseo
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        descripcion = request.POST.get('descripcion')
        disponibilidad = chiva.capacidad
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        esquema = request.POST.get('esquema')
        valor = request.POST.get('valor')

        # Comprobaciones de fecha
        fecha_actual = datetime.now()
        fecha_formato = datetime.strptime(fecha,'%Y-%m-%d').date() 
        hora_formato = datetime.strptime(hora, '%H:%M'). time()
        if (fecha_formato < fecha_actual.date()): # Fecha menor a la actual
            messages.error(request, 'Fecha del paseo no válida.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})
        elif (fecha_formato < fecha_actual.date() + timedelta(2)): # Faltan menos de dos días para la fecha del paseo
            messages.error(request, 'Fecha del paseo no válida. Debes registrar un paseo nuevo con al menos dos días de anticipación.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})
        elif (fecha_formato == fecha_actual.date() + timedelta(2)): # Faltan exactamente dos días, se comprueba la hora
            if (hora_formato < fecha_actual.time()): #Hora menor a la actual, faltan menos de dos días
                messages.error(request, 'Fecha del paseo no válida. Debes registrar un paseo nuevo con al menos dos días de anticipación. Ten en cuenta la hora del paseo.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})

        # Al crear un paseo primero se tiene que crear el esquema de cobro
        # Creamos esquema de cobro
        if esquema == "Aerolínea":
            fechaAumento = request.POST.get('fechaAumento')
            fechaAumento_formato  = datetime.strptime(fechaAumento, '%Y-%m-%d').date() 

            # Comprobaciones fecha de aumento
            if (fechaAumento_formato < fecha_actual.date()): # Fecha de aumento menor a la actual
                messages.error(request, 'Fecha de aumento no válida.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})
            elif (fechaAumento_formato >= fecha_formato - timedelta(1)): #Falta un día o menos a la fecha del paseo
                messages.error(request, 'Fecha de aumento no válida. No puedes aumentar el valor de un paseo faltando un día.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})

            aumento = request.POST.get('aumento')
            esquemaCobro = EsquemaCobro(tipo=esquema,valor=valor, fechaAumento=fechaAumento,valorAumento=aumento,puntoEquilibrio=-1,descuento=-1)

        elif esquema == "Volumen":
            equilibrio = request.POST.get('equilibrio')
            descuento = request.POST.get('descuento')

            # Crear una cadena de texto con la fecha en el formato correcto
            fecha = "2022-12-31"

            # Convertir la cadena de texto en un objeto datetime
            fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d')

            # Obtener solo la parte de la fecha del objeto datetime
            fecha_date = fecha_datetime.date()

            # Crear una nueva instancia de EsquemaCobro con la fecha
            esquemaCobro = EsquemaCobro(tipo=esquema, valor=valor, puntoEquilibrio=equilibrio, descuento=descuento, fechaAumento=fecha_date, valorAumento=-1)
        else:
            messages.error(request, 'Esquema de cobro no válido.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})

        # Leemos contenido de las imagenes
        imagen1 = request.FILES.get('imagen1')
        imagen2 = request.FILES.get('imagen2')
        imagen3 = request.FILES.get('imagen3')
        imagen_base64 = ''

        if not(imagen1) and not(imagen2) and not(imagen3):
            messages.error(request, 'Debes subir al menos una imagen.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas})

        if imagen1:
            imagenContenido = imagen1.read()
            # Convertir el contenido de la imagen a una cadena Base64
            imagen_base64 += base64.b64encode(imagenContenido).decode('utf-8')
            imagen_base64 += "-"
        
        if imagen2:
            imagenContenido = imagen2.read()
            # Convertir el contenido de la imagen a una cadena Base64
            imagen_base64 += base64.b64encode(imagenContenido).decode('utf-8')
            imagen_base64 += "-"
        
        if imagen3:
            imagenContenido = imagen2.read()
            # Convertir el contenido de la imagen a una cadena Base64
            imagen_base64 += base64.b64encode(imagenContenido).decode('utf-8')
            imagen_base64 += "-"

        # Creamos el paseo
        paseo = Paseo(
            origen=origen, fecha=fecha, hora=hora, destino=destino,
            chiva=chiva, descripcion=descripcion,esquemaCobro=esquemaCobro,
            imagen=imagen_base64, disponibilidad=disponibilidad
        )

        # Proceso existoso
        esquemaCobro.save()
        paseo.save()
        # Actualizamos el estado de la chiva escogida
        chiva.estado = 'No Disponible'
        chiva.save()

        messages.success(request, 'Paseo registrado con éxito.')
        return redirect('./')  # Redirigir a la página adecuada después de guardar

    template = loader.get_template('registrarPaseo.html')
    context = {
        'listaChivas': listaChivas,
    }
    return HttpResponse(template.render(context, request))

def verPaseosAdmin(request):
    listaPaseos =  Paseo.objects.all()
    template = loader.get_template('verPaseosAdmin.html')
    context = {
        'listaPaseos': listaPaseos,
    }
    return HttpResponse(template.render(context, request))

def paseoAdmin(request, id):
    try:
        paseo = Paseo.objects.get(pk=id)
        chiva = Chiva.objects.get(pk=paseo.chiva.placa)
        esquema = EsquemaCobro.objects.get(pk=paseo.esquemaCobro.id)
        listaReservas = paseo.reserva_set.all()

    except Paseo.DoesNotExist:
        return messages.error(request,'Paseo no encontrado')

    template = loader.get_template('paseoAdmin.html')
    context = {
        'paseo': paseo,
        'chiva': chiva,
        'esquema': esquema,
        'listaReservas': listaReservas,
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

def hola(request):
    template = loader.get_template('hola.html')
    context = {
        'nombre': 'Mundo'
    }


    return HttpResponse(template.render(context,request))