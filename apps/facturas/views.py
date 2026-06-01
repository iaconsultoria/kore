from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
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
                pass
            else:
                form.save()
                return redirect('revisar_extraccion', pk=factura.pk)

    else:
        form = RevisionFacturaForm(instance=factura)

    return render(request, 'facturas/revisar_extraccion.html', {'form': form, 'factura': factura})

def comprobar_duplicado(request, pk):
    numero = request.GET.get('numero_factura', '')
    proveedor_id = request.GET.get('proveedor', '')

    duplicado = Factura.objects.filter(
        proveedor_id=proveedor_id,
        numero_factura=numero,
    ).exclude(pk=pk).first()

    if duplicado:
        return HttpResponse(
            f"<p><strong>Ya existe una factura con el número {numero} para este proveedor.</strong></p>"
        )
    return HttpResponse("")
