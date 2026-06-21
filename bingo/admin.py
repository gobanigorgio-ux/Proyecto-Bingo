from django.contrib import admin
from .models import TipoSocio, Socio, Prestamo, Pago, MetodoPago, Regalo
from .models import AporteSemanal, CuentaBancaria, Ahorro, Bingo, PartidaBingo
from .models import CartonPartidaBingo, Carton, Jugador, SesionJuego, PlataformaJuego

# Register your models here.
admin.site.register(TipoSocio)
admin.site.register(Socio)
admin.site.register(Prestamo)
admin.site.register(Jugador)

