from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import re


class Tenant(models.Model):
    # Nombre visible de la empresa o cliente
    nombre = models.CharField(max_length=200)

    # Identificador único para URLs y routing
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,  # se genera automáticamente
    )

    # Timestamps de auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    # Activar/desactivar sin eliminar datos
    activo = models.BooleanField(
        default=True,
        db_index=True,  # índice para filtros frecuentes
    )

    def clean(self):
        """
        Validación del slug:
        - Solo minúsculas, números y guiones
        - No puede estar vacío
        """
        if not self.slug:
            raise ValidationError(
                "El slug no puede estar vacío."
            )
        if not re.match(r'^[a-z0-9-]+$', self.slug):
            raise ValidationError(
                "Slug inválido: solo minúsculas, números y guiones."
            )

    def _generar_slug_unico(self):
        """
        Genera un slug único basado en el nombre.
        Si hay colisión, añade un sufijo numérico: empresa, empresa-1, empresa-2...
        """
        base_slug = slugify(self.nombre)
        slug = base_slug
        counter = 1
        while (
            Tenant.objects
            .filter(slug=slug)
            .exclude(pk=self.pk)
            .exists()
        ):
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        """
        Lógica de guardado:
        1. Genera slug automáticamente si no existe
        2. Normaliza a minúsculas
        3. Valida antes de persistir (full_clean)
        """
        if self.nombre and not self.slug:
            self.slug = self._generar_slug_unico()

        self.slug = self.slug.lower()

        self.full_clean()  # dispara clean() y validaciones de campos

        super().save(*args, **kwargs)

    def __str__(self):
        """Representación legible en Django admin"""
        return self.nombre

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["nombre"]
