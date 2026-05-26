from django.db import models

# Create your models here.

from django.db import models


class Factura(models.Model):
    numero_factura = models.CharField(max_length=50)
    fecha_emision = models.DateField()

    nif_emisor = models.CharField(max_length=50)
    nombre_emisor = models.CharField(max_length=200)

    base_imponible = models.DecimalField(max_digits=10, decimal_places=2)
    iva_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    documento_origen = models.FileField(upload_to="facturas/")

    def __str__(self):
        return f"Factura {self.numero_factura}"
