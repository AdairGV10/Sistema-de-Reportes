from django.db import models

class Personal(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    nombre_usuario_perseo = models.CharField(max_length=100, blank=True, null=True)  # Permite valores vacíos y nulos

    def __str__(self):
        return self.name

class PersonalCaja(models.Model):
    SUCURSALES_CHOICES = [
        ('JACALA', 'JACALA'),
        ('ACAXOCHITLAN', 'ACAXOCHITLAN'),
        ('TENANGO', 'TENANGO'),
        ('EL CEREZO', 'EL CEREZO'),
        ('SAN AGUSTIN TLAXIACA', 'SAN AGUSTIN TLAXIACA'),
        ('SAN JOSE TEPENENE', 'SAN JOSE TEPENENE'),
        ('ACTOPAN CIMA', 'ACTOPAN CIMA'),
        ('ACTOPAN OCAMPO', 'ACTOPAN OCAMPO'),
        ('ACTOPAN TUZO', 'ACTOPAN TUZO'),
        ('PROGRESO DE OBREGON', 'PROGRESO DE OBREGON'),
        ('MIXQUIAHUALA', 'MIXQUIAHUALA'),
        ('TUZO MIXQUIAHUALA', 'TUZO MIXQUIAHUALA'),
        ('TLAHUELILPAN', 'TLAHUELILPAN'),
        ('APAXCO TELECABLE', 'APAXCO TELECABLE'),
        ('TEQUIXQUIAC', 'TEQUIXQUIAC'),
    ]

    nombre_completo = models.CharField(max_length=200, blank=True, null=True)  # Permite valores vacíos y nulos
    sucursal = models.CharField(max_length=50, choices=SUCURSALES_CHOICES, blank=True, null=True)  # Permite valores vacíos y nulos
    nombre_usuario_perseo = models.CharField(max_length=100, blank=True, null=True)  # Permite valores vacíos y nulos

    def __str__(self):
        return self.nombre_completo if self.nombre_completo else 'Sin nombre'
    
class Agente(models.Model):
    nombre_usuario_perseo = models.CharField(max_length=100, blank=True, null=True)
