from django.db import models
from django.utils import timezone


class Pedido(models.Model):
    """Modelo para los pedidos"""

    precio_total_sin_impuestos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    precio_total_con_impuestos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def calcular_precio_total(self) -> None:
        """Calcula el precio total del pedido."""

        total_sin_impuestos = sum(
            detalle.articulo_precio_sin_impuestos *
            detalle.cantidad for detalle in self.detallepedido_set.all())
        total_con_impuestos = sum(
            (detalle.articulo_precio_sin_impuestos
                + (detalle.articulo_precio_sin_impuestos
                    * detalle.articulo_impuesto_aplicable / 100))
            * detalle.cantidad for detalle in self.detallepedido_set.all())
        self.precio_total_sin_impuestos = total_sin_impuestos
        self.precio_total_con_impuestos = total_con_impuestos
        self.save()


class DetallePedido(models.Model):
    """Modelo para los detalles de los pedidos."""

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    articulo_id = models.PositiveIntegerField()
    articulo_referencia = models.CharField(max_length=100)
    articulo_nombre = models.CharField(max_length=255)
    articulo_precio_sin_impuestos = models.DecimalField(max_digits=10,
                                                        decimal_places=2)
    articulo_impuesto_aplicable = models.DecimalField(max_digits=5,
                                                      decimal_places=2)
    cantidad = models.PositiveIntegerField()
