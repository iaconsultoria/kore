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
        instance = self.instance
        for field, value in cleaned.items():
            setattr(instance, field, value)
        try:
            instance.clean()
        except forms.ValidationError as e:
            raise e
        return cleaned