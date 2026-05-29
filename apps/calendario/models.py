from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    PRIORIDAD_CHOICES = [
        (1, "Baja"),
        (2, "Media"),
        (3, "Alta")
    ]
    REPROGRAMACION_CHOICES = [
        ("flexible", "Flexible"),
        ("rigida",    "Rígida"),
        ("cancelar",  "Cancelar si no hay hueco"),
    ]
    nombre          = models.CharField(max_length=50, unique=True)
    color           = models.CharField(max_length=7, default="#3B82F6")
    prioridad       = models.PositiveSmallIntegerField(choices=PRIORIDAD_CHOICES, default=2)
    politica_reprog = models.CharField(max_length=20, choices=REPROGRAMACION_CHOICES, default="flexible")
    plantilla_notas = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    PRIORIDAD_CHOICES = [
        (1, "Baja"),
        (2, "Media"),
        (3, "Alta"),
    ]
    REPETIR_CHOICES = [
        ("nunca",   "Nunca"),
        ("diario",  "Diario"),
        ("semanal", "Semanal"),
        ("mensual", "Mensual"),
        ("anual",   "Anual"),
    ]

    titulo = models.CharField(max_length=200)
    inicio      = models.DateField()
    fin         = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)   # ← opcional
    hora_fin    = models.TimeField(null=True, blank=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "citas",
    )
    anotaciones = models.TextField(blank=True, default="")
    prioridad = models.PositiveSmallIntegerField(choices=PRIORIDAD_CHOICES, default=2)
    repetir = models.CharField(max_length=10, choices=REPETIR_CHOICES, default="nunca")
    ubicacion = models.CharField(max_length=255, blank=True, default="")
    def clean(self):
        if self.hora_inicio is None and self.hora_fin is not None:
            raise ValidationError(
                {"hora_fin": "No puede haber hora de fin sin hora de inicio."}
            )
                # Validación de solapamiento: solo si ambas citas tienen hora
        if self.hora_inicio and self.hora_fin and self.inicio and self.fin:
            dt_inicio = datetime.combine(self.inicio, self.hora_inicio)
            dt_fin    = datetime.combine(self.fin,    self.hora_fin)
 
            for otra in Cita.objects.exclude(pk=self.pk).filter(
                hora_inicio__isnull=False,
                hora_fin__isnull=False,
            ):
                otra_dt_inicio = datetime.combine(otra.inicio, otra.hora_inicio)
                otra_dt_fin    = datetime.combine(otra.fin,    otra.hora_fin)
 
                if dt_inicio < otra_dt_fin and dt_fin > otra_dt_inicio:
                    raise ValidationError(
                        f"Esta cita se solapa con «{otra.titulo}» "
                        f"({otra.inicio} {otra.hora_inicio}–{otra.hora_fin}) "
                        f"— prioridad: {otra.get_prioridad_display()}."
                    )
 
    class Meta:
        ordering = ["inicio"]
    
    def __str__(self):
        return self.titulo
    

class Recordatorio(models.Model):
    TIPO_CHOICES = [
        ("notificacion", "Notificación"),
        ("correo",       "Correo electrónico"),
        ]
 
    cita = models.OneToOneField(
        Cita,
        on_delete=models.CASCADE,
        related_name="recordatorio",
    )
    fecha_aviso = models.DateTimeField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default="notificacion")
 
def __str__(self):
     return f"Recordatorio [{self.tipo}]: {self.cita} — {self.fecha_aviso}"

 