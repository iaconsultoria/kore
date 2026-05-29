from django import forms
from .models import Factura


class RevisionFacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'numero_factura',
            'fecha_emision',
            'proveedor',
            'categoria',
            'base_imponible',
            'iva_total',
            'total',
            'archivo_original',
        ]
