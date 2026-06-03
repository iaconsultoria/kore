from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Factura, LineaFactura
from .forms import RevisionFacturaForm
from .utils import buscar_normativa_por_texto
from django.utils import timezone
from datetime import timedelta


def revisar_extraccion(request, pk):
    factura = get_object_or_404(Factura, pk=pk)

    # Obtener primera línea o nombre del proveedor para búsqueda normativa
    primera_linea = factura.lineafactura_set.first()
    texto_busqueda = primera_linea.concepto if primera_linea else factura.proveedor.nombre

    # Buscar fragmentos normativos relevantes
    fragmentos_normativa = buscar_normativa_por_texto(texto_busqueda)

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

    return render(request, 'facturas/revisar_extraccion.html', {
        'form': form,
        'factura': factura,
        'fragmentos_normativa': fragmentos_normativa
    })


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


def avisos_vencimiento(request):
    hoy = timezone.now().date()
    fecha_limite = hoy + timedelta(days=7)

    facturas = Factura.objects.filter(
        fecha_vencimiento__gte=hoy,
        fecha_vencimiento__lte=fecha_limite
    ).order_by('fecha_vencimiento')

    # Marca facturas urgentes que vencen en ≤ 2 días
    for factura in facturas:
        dias_para_vencer = (factura.fecha_vencimiento - hoy).days
        factura.urgente = dias_para_vencer <= 2

    return render(request, 'facturas/avisos_vencimiento.html', {'facturas': facturas})


def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/lista_facturas.html', {'facturas': facturas})


def dashboard_fiscal(request):
    from django.db.models import Sum

    hoy = timezone.now().date()

    # IVA soportado del mes
    lineas_mes = LineaFactura.objects.filter(
        factura__fecha_emision__month=hoy.month,
        factura__fecha_emision__year=hoy.year
    )
    iva_mes = sum(
        (linea.precio_unitario * linea.cantidad * linea.iva_porcentaje / 100)
        for linea in lineas_mes
    )

    # Gastos por categoría
    gastos_por_categoria = Factura.objects.filter(
        categoria__isnull=False
    ).values('categoria__nombre').annotate(
        total=Sum('base_imponible')
    ).order_by('-total')

    # Facturas sin clasificar
    sin_clasificar = Factura.objects.filter(categoria__isnull=True)

    return render(request, 'facturas/dashboard_fiscal.html', {
        'iva_mes': iva_mes,
        'gastos_por_categoria': gastos_por_categoria,
        'sin_clasificar': sin_clasificar
    })
