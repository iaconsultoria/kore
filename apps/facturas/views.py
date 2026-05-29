from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Factura
from .forms import RevisionFacturaForm


def revisar_extraccion(request, pk):
    factura = get_object_or_404(Factura, pk=pk)

    if request.method == 'POST':
        form = RevisionFacturaForm(request.POST, request.FILES, instance=factura)
        if form.is_valid():
            duplicado = Factura.objects.filter(
                proveedor=form.cleaned_data['proveedor'],
                numero_factura=form.cleaned_data['numero_factura'],
            ).exclude(pk=factura.pk).first()

            if duplicado:
                messages.warning(
                    request,
                    f"Ya existe una factura con el número {form.cleaned_data['numero_factura']} para este proveedor."
                )
            else:
                form.save()
                messages.success(request, "Factura guardada correctamente.")
    else:
        form = RevisionFacturaForm(instance=factura)

    return render(request, 'facturas/revisar_extraccion.html', {'form': form, 'factura': factura})
