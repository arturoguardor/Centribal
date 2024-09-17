from decimal import Decimal
from django.db import models
from django.utils import timezone


class Articulo(models.Model):
    """Modelo para los artículos"""

    referencia = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_sin_impuestos = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto_aplicable = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def precio_con_impuestos(self) -> Decimal:
        """Calcula el precio con impuestos"""
        return self.precio_sin_impuestos + (self.precio_sin_impuestos
                                            * self.impuesto_aplicable / 100)

    def __str__(self) -> str:
        return self.nombre
