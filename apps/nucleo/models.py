from django.db import models
from django.core.exceptions import ValidationError


class Negocio(models.Model):
    nombre = models.CharField(max_length=200)

    identificador_fiscal = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    email_contacto = models.EmailField(
        blank=True,
        default=""
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    pais = models.CharField(
        max_length=2,
        default="ES"
    )

    moneda = models.CharField(
        max_length=3,
        default="EUR"
    )

    zona_horaria = models.CharField(
        max_length=50,
        default="Europe/Madrid"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Singleton: solo puede existir un Negocio.

        Hago esto en vez de usar pk=1 fijo porque:
            - No depende de un ID concreto en la base de datos
            - Funciona aunque borres o recrees la base de datos (migraciones)
            - La regla de solo uno queda dentro del propio modelo, no fuera
        """

        if Negocio.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Solo puede existir un Negocio por instalación.")

        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def obtener(cls):
        instancia, _ = cls.objects.get_or_create(
            defaults={
                "nombre": "Mi negocio",
                "pais": "ES",
                "moneda": "EUR",
                "zona_horaria": "Europe/Madrid"
            }
        )
        return instancia

    def __str__(self):
        return self.nombre
