from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from paseos.backends import AdminAuthentication
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

from datetime import datetime, timedelta


import base64


from . forms import ChivaForm
from . forms import PaseoForm
from . forms import PaqueteForm

from .models import Administrador, CuentaBancaria
from .models import Chiva
from .models import Paquete
from .models import Paseo
from .models import EsquemaCobro
from .models import Reserva
from .models import Desembolso
from chivasTravel import settings

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

        # Obtenemos todos los datos del paseo
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        placaChiva = request.POST.get('chiva')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        valor = request.POST.get('valor')
        imagen1 = request.FILES.get('imagen1')
        imagen2 = request.FILES.get('imagen2')
        imagen3 = request.FILES.get('imagen3')
        esquema = request.POST.get('esquema')
        fechaAumento = False
        aumento = False
        equilibrio = False
        descuento = False

        fechaActual = datetime.now()
        fechaFormato = datetime.strptime(fecha,'%Y-%m-%d').date() 
        horaFormato = datetime.strptime(hora, '%H:%M'). time()

        # Necesitamos validar el esquema escogido para obtener todos los datos
        # Al crear un paseo primero se tiene que crear el esquema de cobro
        # Creamos esquema de cobro en caso de que todo este bien
        if esquema == "Aerolínea":
            fechaAumento = request.POST.get('fechaAumento')
            aumento = request.POST.get('aumento')
            fechaAumentoFormato  = datetime.strptime(fechaAumento, '%Y-%m-%d').date() 

            # Comprobaciones fecha de aumento
            if (fechaAumentoFormato < fechaActual.date()): # Fecha de aumento menor a la actual
                messages.error(request, 'Fecha de aumento no válida.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento})
            elif (fechaAumentoFormato >= fechaFormato - timedelta(1)): #Falta un día o menos a la fecha del paseo
                messages.error(request, 'Fecha de aumento no válida. No puedes aumentar el valor de un paseo faltando un día.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento })

            esquemaCobro = EsquemaCobro(tipo=esquema,valor=valor, fechaAumento=fechaAumento,valorAumento=aumento,puntoEquilibrio=-1,descuento=-1)

        elif esquema == "Volumen":
            equilibrio = request.POST.get('equilibrio')
            descuento = request.POST.get('descuento')

            # Comprobaciones equilibrio
            # Primero se obtiene la chiva
            try:
                chiva = Chiva.objects.get(placa=placaChiva)
            except ObjectDoesNotExist:
                messages.error(request,"Por favor seleccione una chiva válida.")
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                    'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                    'equilibrio': equilibrio, 'descuento': descuento})

            if int(equilibrio) > chiva.capacidad: 
                messages.error(request, 'El punto de equilibrio no puede superar la capacidad de la chiva.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                'equilibrio': equilibrio, 'descuento': descuento})

            # Crear una cadena de texto con la fecha en el formato correcto
            fechaVolumen = "2022-12-31"

            # Convertir la cadena de texto en un objeto datetime
            fecha_datetime = datetime.strptime(fechaVolumen, '%Y-%m-%d')

            # Obtener solo la parte de la fecha del objeto datetime
            fecha_date = fecha_datetime.date()

            # Crear una nueva instancia de EsquemaCobro con la fecha
            esquemaCobro = EsquemaCobro(tipo=esquema, valor=valor, puntoEquilibrio=equilibrio, descuento=descuento, fechaAumento=fecha_date, valorAumento=-1)
        else:
            messages.error(request, 'Esquema de cobro no válido.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva})

        # Conseguimos la chiva con la placa y comprobamos que exista
        try:
            chiva = Chiva.objects.get(placa=placaChiva)
        except ObjectDoesNotExist:
            messages.error(request,"Por favor seleccione una chiva válida.")
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                'equilibrio': equilibrio, 'descuento': descuento})

        # Comprobaciones de fecha
        if (fechaFormato < fechaActual.date()): # Fecha menor a la actual
            messages.error(request, 'Fecha del paseo no válida.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                'equilibrio': equilibrio, 'descuento': descuento})
        elif (fechaFormato < fechaActual.date() + timedelta(2)): # Faltan menos de dos días para la fecha del paseo
            messages.error(request, 'Fecha del paseo no válida. Debes registrar un paseo nuevo con al menos dos días de anticipación.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                'equilibrio': equilibrio, 'descuento': descuento})
        elif (fechaFormato == fechaActual.date() + timedelta(2)): # Faltan exactamente dos días, se comprueba la hora
            if (horaFormato < fechaActual.time()): #Hora menor a la actual, faltan menos de dos días
                messages.error(request, 'Fecha del paseo no válida. Debes registrar un paseo nuevo con al menos dos días de anticipación. Ten en cuenta la hora del paseo.')
                return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                'equilibrio': equilibrio, 'descuento': descuento})

        # Leemos contenido de las imagenes
        imagen_base64 = ''

        if not(imagen1) and not(imagen2) and not(imagen3):
            messages.error(request, 'Debes subir al menos una imagen.')
            return render(request, 'registrarPaseo.html', {'listaChivas': listaChivas, 'origen': origen, 'destino':destino, 'descripcion': descripcion, 'fecha': fecha,
                'hora': hora, 'esquema': esquema, 'valor': valor, 'placaChiva': placaChiva, 'fechaAumento': fechaAumento, 'aumento': aumento,
                'equilibrio': equilibrio, 'descuento': descuento})

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
        disponibilidad = chiva.capacidad
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
        chiva = Chiva.objects.get(pk=paseo.chiva.id)
        esquema = EsquemaCobro.objects.get(pk=paseo.esquemaCobro.id)
        listaReservas = paseo.reserva_set.all()
        # for reserva in listaReservas:
        #     reserva.persona_id= reserva.persona

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

# Registro de una chiva

def chivas(request):
    listaChivas = Chiva.objects.all()

    if request.method == 'POST':
        form = ChivaForm(request.POST)
        chivaPlaca = request.POST.get("placa")
        chivaCapacidad = request.POST.get("capacidad")
        chivaTipo = request.POST.get("tipo")
        chivaEstado = request.POST.get("estado")
        
        # Verificación de que no este registrada la placa

        if  Chiva.objects.filter(placa = chivaPlaca ).exists():
            messages.error(request, 'La placa de la chiva ya se encuentra registrada.')
            return render(request, 'chivas.html', {
                'listaChivas': listaChivas, 
                'chivaPlaca' : chivaPlaca, 
                'chivaCapacidad' : chivaCapacidad,
                'chivaTipo' : chivaTipo, 
                'chivaEstado' : chivaEstado })
        
        # Verificación tipo de chiva elegido en el formulario

        if (chivaTipo == 'Normal') or (chivaTipo =='Rumbera'):
            pass
        else:
            messages.error(request, 'Tipo de chiva no válido.')
            return render(request, 'chivas.html', {
                'listaChivas': listaChivas, 
                'chivaPlaca' : chivaPlaca, 
                'chivaCapacidad' : chivaCapacidad,
                'chivaTipo' : chivaTipo, 
                'chivaEstado' : chivaEstado })
        
        # Verificación estado de chiva elegido en el formulario

        if (chivaEstado == 'Disponible') or (chivaEstado =='No Disponible'):
            pass
        else:
            messages.error(request, 'Estado de chiva no válido.')
            return render(request, 'chivas.html', {
                'listaChivas': listaChivas, 
                'chivaPlaca' : chivaPlaca, 
                'chivaCapacidad' : chivaCapacidad, 
                'chivaTipo' : chivaTipo,
                'chivaEstado' : chivaEstado
                 })    

        # Registro exitoso de la chiva

        if form.is_valid():
            form.save()
            messages.success(request, 'Chiva registrada con éxito')
        else:
            print(form.errors)  
            messages.error(request, 'Error al registrar la chiva.')
           
    else:
        form = ChivaForm()

    template = loader.get_template('chivas.html')
    context = {
        'listaChivas': listaChivas,
        'form': form,
        'actualización': None
    }
    return HttpResponse(template.render(context, request))

# Actualización de los datos de una chiva

def actualizarFormChiva(request, id):
    chiva = get_object_or_404(Chiva, pk=id)
    listaChivas = Chiva.objects.all()
    paseoChiva = None

    # Chivas asociadas a un paseo 

    try:
        paseoChiva = Paseo.objects.get(chiva_id=id)
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        chivaPlaca = request.POST.get("placa")
        chivaCapacidad = request.POST.get("capacidad")
        chivaTipo = request.POST.get("tipo")
        chivaEstado = request.POST.get("estado")

        chiva.placa = chivaPlaca
        chiva.capacidad = chivaCapacidad
        chiva.tipo = chivaTipo
        chiva.estado = chivaEstado

        # La modificación de la placa no puede ser por una ya existente 

        if  Chiva.objects.filter(placa = chiva.placa ).exclude(pk=id).exists():
                messages.error(request, 'La placa de la chiva ya se encuentra registrada.')
                return render(request, 'chivas.html', {
                    'listaChivas': listaChivas, 
                    'actualizacion': chiva,
                    'paseoChiva': paseoChiva})
        
        chiva.save()

        messages.success(request, 'Chiva actualizada con éxito')
        return redirect('chivas')
    else:
        form = ChivaForm(instance=chiva) 

    context = {
        'listaChivas': listaChivas,
        'form': form,
        'actualizacion': chiva,
        'paseoChiva': paseoChiva
    }
    return render(request, 'chivas.html', context)

def eliminarChiva(request, id):
    try:
        chiva = Chiva.objects.get(pk=id)
    except Chiva.DoesNotExist:
        return messages.error('Chiva no encontrada')
    
    # Las chivas asociadas a un paseo no pueden ser eliminadas 

    if Paseo.objects.filter(chiva_id=id).exists():
        messages.error(request, 'Error al eliminar la chiva, esta se encuentra asociada a un paseo')
    else:
        chiva.delete()
        messages.warning(request, 'Chiva eliminada con éxito')
  
    return redirect('../')

# Registro de un paquete 

def paquetes(request):
    listaPaquetes = Paquete.objects.all()
    

    if request.method == 'POST':
        form = PaqueteForm(request.POST)
        paqueteNombre = request.POST.get("nombre")
        paqueteDescripcion = request.POST.get("descripcion")
        paqueteValor = request.POST.get("valor")
        
        
        # Registro exitoso de la Paquete

        if form.is_valid():
            form.save()
            messages.success(request, 'Paquete registrado con éxito')
        else:
            print(form.errors)  
            messages.error(request, 'Error al registrar el paquete.')
           
    else:
        form = PaqueteForm()

    template = loader.get_template('paquetes.html')
    context = {
        'listaPaquetes': listaPaquetes,
        'form': form,
        'actualización': None
    }
    return HttpResponse(template.render(context, request))

#  

def actualizarFormPaquete(request, id):
    paquete = get_object_or_404(Paquete, pk=id)
    listaPaquetes = Paquete.objects.all()
    

    if request.method == 'POST':
        paqueteNombre = request.POST.get("nombre")
        paqueteDescripcion = request.POST.get("descripcion")
        paqueteValor = request.POST.get("valor")

        paquete.nombre = paqueteNombre
        paquete.descripcion = paqueteDescripcion
        paquete.valor = paqueteValor
        
        paquete.save()

        messages.success(request, 'Paquete actualizado con éxito')
        return redirect('paquetes')
    else:
        form = PaqueteForm(instance=paquete) 

   
    context = {
        'listaPaquetes': listaPaquetes,
        'form': form,
        'actualizacion': paquete,
        
    }
    return render(request, 'paquetes.html', context)

def eliminarPaquete(request, id):

    try:
        paquete = Paquete.objects.get(pk=id)
    except Paquete.DoesNotExist:
        return messages.error('Paquete no encontrado')
    
    # Los paquetes asociados a una reserva no pueden ser eliminados

    if Reserva.objects.filter(paquete_id=id).exists():
        messages.error(request, 'Error al eliminar el Paquete, este se encuentra asociado a un reserva')
    else:
        paquete.delete()
        messages.warning(request, 'Paquete eliminado con éxito')
  
    return redirect('../')



def pagosAdmin(request):
    pendientes = Reserva.objects.filter(estado="pendientePago")
    confirmadas = Reserva.objects.filter(estado="confirmada")

    lista = request.GET.get('lista', 'confirmadas')

    if lista == 'pendientes':
        listaReservas = pendientes
    else:
        listaReservas = confirmadas

    paginator = Paginator(listaReservas, 10)

    pageNumber = request.GET.get('page')
    objsReserva = paginator.get_page(pageNumber)

    if request.method == "POST":
        reservaID = request.POST.get('reservaID')
        action = request.POST.get('action')

        try:
            reservaElegida = Reserva.objects.get(id=reservaID)

            if action == 'confirmar':
                reservaElegida.estado = 'confirmada'
                messages.success(request, f"Reserva No. {reservaElegida.id} confirmada")
            elif action == 'rechazar':
                reservaElegida.estado = 'pendientePago'
                messages.error(request, f"Reserva No. {reservaElegida.id} rechazada")
            reservaElegida.save()
        except Reserva.DoesNotExist:
            messages.error(request, 'No se ha encontrado la reserva.')
        return redirect('pagosAdmin')
    
    return render(request, 'pagosAdmin.html', {'listaReservas' : objsReserva,
                                               'lista' : lista})

def desembolsos(request):

    # Verificamos si existen registros de desembolsos
    template = loader.get_template('desembolsos.html')

    if (len(Desembolso.objects.all()) > 0):

        # Verificamos que lista se quiere
        lista = request.GET.get('lista', 'pendientes')
        if lista == 'pendientes':
            listaDesembolsos = Desembolso.objects.filter(estado='pendiente')
            check = False
        else:
            listaDesembolsos = Desembolso.objects.filter(estado='completado')
            check = True

        # Paginacion
        paginator = Paginator(listaDesembolsos, 10)
        pageNumber = request.GET.get('page')
        objsDesembolso = paginator.get_page(pageNumber)
            
        if request.method == 'POST':

            desembolsoID = request.POST.get('desembolsoID')
            comprobante = request.FILES.get('comprobante')
    
            # Comprobamos si el admin subió el comprobante de devolución
            if (comprobante): 

                # Obtenemos el objeto desembolso para actualizar su estado y guardar el comprobante
                desembolso = Desembolso.objects.get(id=desembolsoID)
                desembolso.estado = 'completado'

                # Codificamos la imagen
                imagen_base64 = ''
                imagenContenido = comprobante.read()
                # Convertir el contenido de la imagen a una cadena Base64
                imagen_base64 = base64.b64encode(imagenContenido).decode('utf-8')
                desembolso.comprobante = imagen_base64

                #Actualizamos el estado de la reserva
                reserva = desembolso.reserva
                reserva.estado = 'desembolsada'

                reserva.save()
                desembolso.save()

                # Notificamos por correo electronico
                email = desembolso.reserva.persona.correo
                templateEmail = loader.get_template('emailDesembolso.html')
                try:
                    paquete = desembolso.reserva.paquete.nombre
                except:
                    paquete = desembolso.reserva.paquete

                content = templateEmail.render({'motivo': desembolso.motivo, 'monto': desembolso.monto,
                'cliente': desembolso.reserva.persona.nombre, 'id': desembolso.reserva.persona.id, 'correo': desembolso.reserva.persona.correo,
                'celular': desembolso.reserva.persona.celular, 'cuenta': f'{desembolso.reserva.persona.cuentaBancaria.numCuenta} - {desembolso.reserva.persona.cuentaBancaria.tipoCuente}',
                'entidad': desembolso.reserva.persona.cuentaBancaria.entidadBancaria, 'paseo': f'{desembolso.reserva.paseo.origen} - {desembolso.reserva.paseo.destino}', 
                'fecha': desembolso.reserva.fechaCreacion, 'paquete': paquete, 'valor': desembolso.reserva.valor})

                msg = EmailMultiAlternatives(
                    'Notificación de desembolso',
                    'Hemos desembolsado tu dinero.',
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                msg.attach_alternative(content, 'text/html')
                #Adjuntar la imagen
                img = MIMEImage(imagenContenido)
                img.add_header('Content-Disposition', 'attachment', filename=f'ComprobanteDesembolso{desembolso.reserva.persona.id}')
                msg.attach(img)
                msg.send()

                messages.success(request, 'Desembolso realizado con éxito. El cliente ha sido informado del proceso por correo electrónico.')
                return render(request, 'desembolsos.html', { 'listaDesembolsos': objsDesembolso, 'lista': lista,
                'check': check})
            else:
                messages.error(request, 'Debes subir el comprobante de devolución.')
                return render(request, 'desembolsos.html', { 'listaDesembolsos': objsDesembolso, 'lista': lista,
                'check': check})

        context = {
            'listaDesembolsos': objsDesembolso,
            'lista': lista,
            'check': check
        }

        return HttpResponse(template.render(context, request))
    else:

        context = {
            'sinDesembolsos': True
        }
        return HttpResponse(template.render(context, request))
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paseo, Cliente, CuentaBancaria

@csrf_exempt
def crearReserva(request):
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')
        edad = request.POST.get('edad')
        numCuenta = request.POST.get('numCuenta')
        tipoCuente = request.POST.get('tipoCuente')
        entidadBancaria = request.POST.get('entidadBancaria')
        paseo_id = request.POST.get('paseo_id')
        
        paseo = Paseo.objects.get(id=paseo_id)

        cuenta_bancaria, created = CuentaBancaria.objects.get_or_create(
            numCuenta=numCuenta,
            defaults={'tipoCuente': tipoCuente, 'entidadBancaria': entidadBancaria}
        )
        if not created:
            cuenta_bancaria.tipoCuente = tipoCuente
            cuenta_bancaria.entidadBancaria = entidadBancaria
            cuenta_bancaria.save()

        cliente = Cliente(
            id=identificacion,
            nombre=f"{nombres} {apellidos}",
            celular=celular,
            correo=correo,
            edad=edad,
            cuentaBancaria=cuenta_bancaria,
            rol='cliente'
        )
        cliente.save()

        return JsonResponse({'success': True})

    listaPaseos = Paseo.objects.all()
    context = {'listaPaseos': listaPaseos}
    return render(request, 'crearReserva.html', context)

def misReservas(request):
    template = loader.get_template('misReservas.html')
    context = {}
    return HttpResponse(template.render(context, request))