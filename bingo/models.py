from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

# =========================================================================
# CLASE 1: TIPO DE SOCIO
# =========================================================================
class TipoSocio(models.Model):
    idtiposocio = models.AutoField(primary_key=True)
    nombretiposocio = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Socio")
    roltiposocio = models.CharField(max_length=50, unique=True, verbose_name="Rol del Socio")
    descripciondetiposocio = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        return f"{self.nombretiposocio} ({self.roltiposocio})"

    class Meta:
        db_table = 'TipoSocio'
        verbose_name = 'Tipo de Socio'
        verbose_name_plural = 'Tipos de Socio'


# =========================================================================
# CLASE 2: SOCIO
# =========================================================================
class Socio(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    idsocio = models.AutoField(primary_key=True)
    cedulasocio = models.CharField(max_length=10, unique=True, verbose_name="Cédula de Identidad")
    nombresocio = models.CharField(max_length=100, verbose_name="Nombres")
    apellidosocio = models.CharField(max_length=100, verbose_name="Apellidos")
    fechanacimientosocio = models.DateField(verbose_name="Fecha de Nacimiento")
    telefonosocio = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    correosocio = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    direccionsocio = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dirección")
    fechaingresosocio = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    estadosocio = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Activo', verbose_name="Estado")
    
    idtiposocio = models.ForeignKey(TipoSocio, on_delete=models.CASCADE, db_column='idtiposocio', verbose_name="Tipo de Socio")

    def __str__(self):
        return f"{self.nombresocio} {self.apellidosocio} - {self.cedulasocio}"

    class Meta:
        db_table = 'Socio'
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'


# =========================================================================
# CLASE 3: PRÉSTAMO
# =========================================================================
class Prestamo(models.Model):
    ESTADO_PRESTAMO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Pagado', 'Pagado'),
        ('Rechazado', 'Rechazado'),
    ]

    idprestamo = models.AutoField(primary_key=True)
    montoprestamo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Solicitado")
    tasainteres = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa de Interés (%)")
    plazomeses = models.IntegerField(verbose_name="Plazo en Meses")
    fechasolicitud = models.DateField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    fechaaprobacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Aprobación")
    estadoprestamo = models.CharField(max_length=20, choices=ESTADO_PRESTAMO_CHOICES, default='Pendiente', verbose_name="Estado del Préstamo")
    
    idsocio = models.ForeignKey(Socio, on_delete=models.CASCADE, db_column='idsocio', verbose_name="Socio")

    def __str__(self):
        return f"Préstamo #{self.idprestamo} - {self.idsocio.nombresocio} ({self.montoprestamo})"

    class Meta:
        db_table = 'Prestamo'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'


# =========================================================================
# CLASE 4: PAGO
# =========================================================================
class Pago(models.Model):
    idpago = models.AutoField(primary_key=True)
    montopago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    fechapago = models.DateField(auto_now_add=True, verbose_name="Fecha de Pago")
    
    idprestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, db_column='idprestamo', verbose_name="Préstamo")

    def __str__(self):
        return f"Pago #{self.idpago} - Préstamo #{self.idprestamo.idprestamo} ({self.montopago})"

    class Meta:
        db_table = 'Pago'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'


# =========================================================================
# CLASE 5: MÉTODO DE PAGO
# =========================================================================
class MetodoPago(models.Model):
    idmetodopago = models.AutoField(primary_key=True)
    nombremetodopago = models.CharField(max_length=50, unique=True, verbose_name="Método de Pago")
    detallesmetodopago = models.CharField(max_length=200, null=True, blank=True, verbose_name="Detalles Opcionales")

    def __str__(self):
        return self.nombremetodopago

    class Meta:
        db_table = 'MetodoPago'
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'


# =========================================================================
# CLASE 6: REGALO
# =========================================================================
class Regalo(models.Model):
    idregalo = models.AutoField(primary_key=True)
    nombreregalo = models.CharField(max_length=100, verbose_name="Nombre del Regalo / Incentivo")
    descripcionregalo = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción")
    fecharegalo = models.DateField(auto_now_add=True, verbose_name="Fecha de Entrega")
    
    idsocio = models.ForeignKey(Socio, on_delete=models.CASCADE, db_column='idsocio', verbose_name="Socio Beneficiario")

    def __str__(self):
        return f"Regalo: {self.nombreregalo} para {self.idsocio.nombresocio}"

    class Meta:
        db_table = 'Regalo'
        verbose_name = 'Regalo'
        verbose_name_plural = 'Regalos'


# =========================================================================
# CLASE 7: APORTE SEMANAL
# =========================================================================
class AporteSemanal(models.Model):
    idaportesemanal = models.AutoField(primary_key=True)
    montoaporte = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto del Aporte")
    fechapagoaporte = models.DateField(auto_now_add=True, verbose_name="Fecha de Pago")
    
    idsocio = models.ForeignKey(Socio, on_delete=models.CASCADE, db_column='idsocio', verbose_name="Socio")

    def __str__(self):
        return f"Aporte Semanal #{self.idaportesemanal} - {self.idsocio.nombresocio}"

    class Meta:
        db_table = 'AporteSemanal'
        verbose_name = 'Aporte Semanal'
        verbose_name_plural = 'Aportes Semanales'


# =========================================================================
# CLASE 8: CUENTA BANCARIA
# =========================================================================
class CuentaBancaria(models.Model):
    idcuentabancaria = models.AutoField(primary_key=True)
    nombrebanco = models.CharField(max_length=100, verbose_name="Nombre del Banco")
    numerocuenta = models.CharField(max_length=50, unique=True, verbose_name="Número de Cuenta")
    tipocuenta = models.CharField(max_length=50, verbose_name="Tipo de Cuenta (Ahorros/Corriente)")

    def __str__(self):
        return f"{self.nombrebanco} - {self.numerocuenta}"

    class Meta:
        db_table = 'CuentaBancaria'
        verbose_name = 'Cuenta Bancaria'
        verbose_name_plural = 'Cuentas Bancarias'


# =========================================================================
# CLASE 9: AHORRO
# =========================================================================
class Ahorro(models.Model):
    idahorro = models.AutoField(primary_key=True)
    montoahorro = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Ahorrado")
    fechaahorro = models.DateField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    idsocio = models.ForeignKey(Socio, on_delete=models.CASCADE, db_column='idsocio', verbose_name="Socio")

    def __str__(self):
        return f"Ahorro #{self.idahorro} - {self.idsocio.nombresocio} ({self.montoahorro})"

    class Meta:
        db_table = 'Ahorro'
        verbose_name = 'Ahorro'
        verbose_name_plural = 'Ahorros'


# =========================================================================
# CLASE 10: BINGO
# =========================================================================
class Bingo(models.Model):
    idbingo = models.AutoField(primary_key=True)
    nombrebingo = models.CharField(max_length=100, verbose_name="Nombre del Evento Bingo")
    fechabingo = models.DateField(verbose_name="Fecha del Bingo")

    def __str__(self):
        return self.nombrebingo

    class Meta:
        db_table = 'Bingo'
        verbose_name = 'Bingo'
        verbose_name_plural = 'Bingos'


# =========================================================================
# CLASE 11: PARTIDA DE BINGO
# =========================================================================
class PartidaBingo(models.Model):
    idpartidabingo = models.AutoField(primary_key=True)
    horainicio = models.TimeField(verbose_name="Hora de Inicio")
    premio = models.CharField(max_length=200, verbose_name="Premio de la Partida")
    
    idbingo = models.ForeignKey(Bingo, on_delete=models.CASCADE, db_column='idbingo', verbose_name="Bingo")

    def __str__(self):
        return f"Partida #{self.idpartidabingo} - Bingo: {self.idbingo.nombrebingo}"

    class Meta:
        db_table = 'PartidaBingo'
        verbose_name = 'Partida de Bingo'
        verbose_name_plural = 'Partidas de Bingo'


# =========================================================================
# CLASE 12: CARTÓN PARTIDA BINGO
# =========================================================================
class CartonPartidaBingo(models.Model):
    idcartonpartidabingo = models.AutoField(primary_key=True)
    estadocarton = models.CharField(max_length=50, default="Disponible", verbose_name="Estado del Cartón")
    
    idpartidabingo = models.ForeignKey(PartidaBingo, on_delete=models.CASCADE, db_column='idpartidabingo', verbose_name="Partida de Bingo")

    def __str__(self):
        return f"Cartón-Partida #{self.idcartonpartidabingo} - Estado: {self.estadocarton}"

    class Meta:
        db_table = 'CartonPartidaBingo'
        verbose_name = 'Cartón en Partida'
        verbose_name_plural = 'Cartones en Partidas'


# =========================================================================
# CLASE 13: CARTÓN
# =========================================================================
class Carton(models.Model):
    idcarton = models.AutoField(primary_key=True)
    numerocarton = models.IntegerField(unique=True, verbose_name="Número de Cartón Único")

    def __str__(self):
        return f"Cartón N° {self.numerocarton}"

    class Meta:
        db_table = 'Carton'
        verbose_name = 'Cartón'
        verbose_name_plural = 'Cartones'


# =========================================================================
# CLASE 14: JUGADOR
# =========================================================================
class Jugador(models.Model):
    idjugador = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario del Sistema")
    nombrejugador = models.CharField(max_length=100, verbose_name="Nombre del Jugador")

    def __str__(self):
        return self.nombrejugador

    class Meta:
        db_table = 'Jugador'
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'


# =========================================================================
# CLASE 15: SESIÓN DE JUEGO
# =========================================================================
class SesionJuego(models.Model):
    idsesionjuego = models.AutoField(primary_key=True)
    fechasesion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora de Sesión")
    
    idjugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='idjugador', verbose_name="Jugador")

    def __str__(self):
        return f"Sesión #{self.idsesionjuego} - {self.idjugador.nombrejugador}"

    class Meta:
        db_table = 'SesionJuego'
        verbose_name = 'Sesión de Juego'
        verbose_name_plural = 'Sesiones de Juego'


# =========================================================================
# CLASE 16: PLATAFORMA DE JUEGO
# =========================================================================
class PlataformaJuego(models.Model):
    idplataformajuego = models.AutoField(primary_key=True)
    nombreplataforma = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Plataforma")

    def __str__(self):
        return self.nombreplataforma

    class Meta:
        db_table = 'PlataformaJuego'
        verbose_name = 'Plataforma de Juego'
        verbose_name_plural = 'Plataformas de Juego'