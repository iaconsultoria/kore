from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError


validador_nif = RegexValidator(
    regex=r'^[0-9XYZ][0-9]{7}[A-Z]$|^[ABCDEFGHJKLMNPQRSUVW][0-9]{7}[0-9A-J]$',
    message="Introduce un NIF, NIE o CIF español válido."
)


def validar_tamanio_archivo(archivo):
    if archivo.size > 10 * 1024 * 1024:
        raise ValidationError("El archivo no puede superar 10 MB.")


class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=200)
    deducible_iva = models.BooleanField(default=True)
    cuenta_contable = models.CharField(max_length=10, blank=True, default="")

    class Meta:
        verbose_name = "Categoría de gasto"
        verbose_name_plural = "Categorías de gasto"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    nif = models.CharField(max_length=20, validators=[validador_nif])
    direccion = models.TextField(blank=True, default="")
    pais = models.CharField(max_length=2, default="ES")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


IVA_CHOICES = [
    (21, "21 %"),
    (10, "10 %"),
    (4,  "4 %"),
    (0,  "0 %"),
]


class Factura(models.Model):
    numero_factura = models.CharField(max_length=50) # numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    categoria = models.ForeignKey(
        CategoriaGasto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    base_imponible = models.DecimalField(max_digits=10, decimal_places=2)
    iva_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    archivo_original = models.FileField(
        upload_to="facturas/%Y/%m/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "jpg", "jpeg", "png"]),
            validar_tamanio_archivo,
        ]
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        #ordering = ["-fecha_emision"]

    def __str__(self):
        return f"Factura {self.numero_factura}"


class LineaFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_porcentaje = models.IntegerField(choices=IVA_CHOICES, default=21)

    # total_linea se calcula como property y no se guarda en BD.
    # Guardarlo sería algo redundante ya que si cambia cantidad o precio
    # habría que actualizarlo en dos sitios con riesgo de inconsistencia
    @property
    def total_linea(self):
        return self.cantidad * self.precio_unitario * (1 + self.iva_porcentaje / 100)

    class Meta:
        verbose_name = "Línea de factura"
        verbose_name_plural = "Líneas de factura"

    def __str__(self):
        return f"{self.concepto} ({self.cantidad} × {self.precio_unitario})"
