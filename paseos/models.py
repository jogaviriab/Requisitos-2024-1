from django.db import models

# Create your models here.
class CuentaBancaria(models.Model):
    numCuenta = models.IntegerField()
    tipoCuente = models.CharField(max_length=100)
    entidadBancaria = models.CharField(max_length=100)

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    celular = models.IntegerField()
    correo = models.EmailField()
    edad = models.IntegerField()
    rol = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    celular = models.IntegerField()
    correo = models.EmailField()
    edad = models.IntegerField()
    rol = models.CharField(max_length=100)
    cuentaBancaria = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE)

class Chiva(models.Model):
    placa = models.CharField(primary_key=True,max_length=100)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

class EsquemaCobro(models.Model):
    tipo = models.CharField(max_length=100)
    valor = models.IntegerField(default=0)
    puntoEquilibrio = models.IntegerField()
    valorAumento = models.IntegerField()
    fechaAumento = models.DateField()
    descuento = models.IntegerField()

class Paseo(models.Model):
    imagen = models.CharField(max_length=500, default='default_value')
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    fecha = models.DateField()
    hora = models.TimeField()
    chiva = models.ForeignKey(Chiva, on_delete=models.CASCADE)
    esquemaCobro = models.ForeignKey(EsquemaCobro, on_delete=models.CASCADE)
    disponibilidad = models.IntegerField()

class Paquete(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    valor = models.IntegerField()

class Reserva(models.Model):
    paseo = models.ForeignKey(Paseo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)
    fechaCreacion = models.DateField()
    valor = models.IntegerField()
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    comprobantePago = models.CharField(max_length=200)
    persona = models.ForeignKey(Cliente, on_delete=models.CASCADE)


