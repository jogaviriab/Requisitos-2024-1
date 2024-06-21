from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Create your models here.
class CuentaBancaria(models.Model):
    numCuenta = models.IntegerField()
    tipoCuente = models.CharField(max_length=100)
    entidadBancaria = models.CharField(max_length=100)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    celular = models.IntegerField()
    correo = models.EmailField()
    edad = models.IntegerField()
    rol = models.CharField(max_length=100)
    cuentaBancaria = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE)


class Chiva(models.Model):
    placa = models.CharField( max_length=100, unique=True )
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


class AdministradorManager(BaseUserManager):
    def create_user(self, nombre, correo, celular, edad, rol, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico debe ser proporcionado')

        user = self.model(
            nombre=nombre,
            correo=self.normalize_email(correo),
            celular=celular,
            edad=edad,
            rol=rol,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre, correo, celular, edad, rol, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nombre, correo, celular, edad, rol, password, **extra_fields)

class Administrador(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    celular = models.IntegerField()
    correo = models.EmailField(unique=True)
    edad = models.IntegerField()
    rol = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'celular', 'edad', 'rol', 'password', 'id']

    objects = AdministradorManager()


    
    def __str__(self):
        return self.nombre

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff