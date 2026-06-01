from django import forms
from .models import Cita
 
 
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            "titulo", "inicio", "fin",
            "hora_inicio", "hora_fin",
            "categoria", "prioridad",
            "repetir", "ubicacion", "anotaciones",
        ]
        widgets = {
            "inicio":      forms.DateInput(attrs={"type": "date"}),
            "fin":         forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fin":    forms.TimeInput(attrs={"type": "time"}),
        }
 
    def clean(self):
        cleaned = super().clean()
        hora_inicio = cleaned.get("hora_inicio")
        hora_fin    = cleaned.get("hora_fin")
        inicio      = cleaned.get("inicio")
        fin         = cleaned.get("fin")

        if hora_inicio and hora_fin and inicio and fin:
            from datetime import datetime
            dt_inicio = datetime.combine(inicio, hora_inicio)
            dt_fin    = datetime.combine(fin, hora_fin)

            from .models import Cita
            for otra in Cita.objects.exclude(pk=self.instance.pk).filter(
                hora_inicio__isnull=False,
                hora_fin__isnull=False,
            ):
                otra_dt_inicio = datetime.combine(otra.inicio, otra.hora_inicio)
                otra_dt_fin    = datetime.combine(otra.fin,    otra.hora_fin)

                if dt_inicio < otra_dt_fin and dt_fin > otra_dt_inicio:
                    raise forms.ValidationError(
                        f"Esta cita se solapa con «{otra.titulo}» "
                        f"({otra.inicio} {otra.hora_inicio}–{otra.hora_fin}) "
                        f"— prioridad: {otra.get_prioridad_display()}."
                    )
        return cleaned