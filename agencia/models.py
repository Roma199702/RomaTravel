from django.db import models
from django.core.validators import MinValueValidator


class Viaje(models.Model):

    TIPOS_VIAJE = [
        ('Nacional', 'Nacional'),
        ('Internacional', 'Internacional'),
        ('Aventura', 'Aventura'),
        ('Playa', 'Playa'),
        ('Cultural', 'Cultural'),
    ]

    destino = models.CharField(
        max_length=100
    )

    pais = models.CharField(
        max_length=100
    )

    fecha_salida = models.DateField()

    fecha_regreso = models.DateField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[
            MinValueValidator(1)
        ]
    )

    cupos = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )

    tipo_viaje = models.CharField(
        max_length=30,
        choices=TIPOS_VIAJE
    )

    descripcion = models.TextField(
        max_length=500
    )

    def __str__(self):
        return f"{self.destino} - {self.pais}"


class Reserva(models.Model):

    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    nombre = models.CharField(
        max_length=100
    )

    rut = models.CharField(
        max_length=12
    )

    correo = models.EmailField()

    cantidad_personas = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    precio_total = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    fecha_reserva = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.viaje.destino}"