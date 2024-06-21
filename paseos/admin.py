from django.contrib import admin

from .models import Administrador
from .models import Chiva
from .models import EsquemaCobro
from .models import Cliente
from .models import CuentaBancaria
from .models import Reserva
from .models import Paquete
from .models import Paseo
from .models import Desembolso
# Register your models here.

admin.site.register(Administrador)
admin.site.register(Chiva)
admin.site.register(EsquemaCobro)
admin.site.register(Paseo)
admin.site.register(Cliente)
admin.site.register(CuentaBancaria)
admin.site.register(Reserva)
admin.site.register(Paquete)
admin.site.register(Desembolso)