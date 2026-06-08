from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Factura, LineaFactura, CategoriaGasto, SugerenciaCategoria
from .forms import RevisionFacturaForm
from .utils import buscar_normativa_por_texto, sugerir_categoria
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def revisar_extraccion(request, pk):
    factura = get_object_or_404(Factura, pk=pk)

    if factura.extraccion_fallida:
        return render(request, 'facturas/revisar_extraccion.html', {
            'factura': factura,
            'error_extraccion': factura.error_extraccion,
            'form': None
        })

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


def sugerir_categoria_view(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    lineas = factura.lineafactura_set.all()

    try:
        sugerencia = sugerir_categoria(factura.proveedor.nombre, lineas)

        registro = SugerenciaCategoria.objects.create(
            factura=factura,
            texto_sugerencia=sugerencia,
            modelo_ia_usado="claude-sonnet-4-20250514",
            aceptada=None
        )

        html = f"""
        <div style="background-color: #fff3cd; padding: 15px; margin-top: 10px; border-left: 4px solid #ffc107;">
            <p><strong>Sugerencia:</strong> {sugerencia}</p>
            <button hx-post="/facturas/revisar/{pk}/aceptar-sugerencia/" hx-vals='{{"sugerencia": "{sugerencia}", "sugerencia_id": "{registro.pk}"}}' hx-target="#sugerencia-categoria" hx-swap="innerHTML" style="padding: 5px 10px; background-color: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px;">Aceptar</button>
            <button hx-post="/facturas/revisar/{pk}/ignorar-sugerencia/" hx-vals='{{"sugerencia_id": "{registro.pk}"}}' hx-target="#sugerencia-categoria" hx-swap="innerHTML" style="padding: 5px 10px; background-color: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">Ignorar</button>
        </div>
        """
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<p>Error al sugerir: {str(e)}</p>")

@require_POST
def aceptar_sugerencia_view(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    nombre = request.POST.get('sugerencia', '').strip()
    sugerencia_id = request.POST.get('sugerencia_id')

    if not nombre:
        return HttpResponse('<p>Error: sugerencia vacía.</p>')

    categoria, _ = CategoriaGasto.objects.get_or_create(nombre=nombre)
    factura.categoria = categoria
    factura.save()

    if sugerencia_id:
        SugerenciaCategoria.objects.filter(pk=sugerencia_id).update(aceptada=True)

    return HttpResponse(
        f'<div style="background-color:#d4edda; padding:15px; margin-top:10px; border-left:4px solid #28a745;">'
        f'<p>Categoría <strong>{nombre}</strong> asignada correctamente.</p>'
        f'</div>'
    )


@require_POST
def ignorar_sugerencia_view(request, pk):
    sugerencia_id = request.POST.get('sugerencia_id')
    if sugerencia_id:
            SugerenciaCategoria.objects.filter(pk=sugerencia_id).update(aceptada=False)
    return HttpResponse("")


@csrf_exempt
@require_http_methods(["POST"])
def mcp_endpoint(request):
    """Endpoint MCP que maneja llamadas a herramientas."""
    try:
        body = json.loads(request.body)

        tool_name = body.get("name")
        arguments = body.get("arguments", {})

        if tool_name == "listar_facturas":
            limit = arguments.get("limit", 10)
            facturas = Factura.objects.select_related("proveedor", "categoria").order_by("-fecha_emision")[:limit]
            resultado = []
            for f in facturas:
                resultado.append({
                    "id": f.id,
                    "numero_factura": f.numero_factura,
                    "proveedor": f.proveedor.nombre,
                    "fecha_emision": f.fecha_emision.isoformat(),
                    "total": float(f.total),
                    "categoria": f.categoria.nombre if f.categoria else None
                })
            return JsonResponse({"resultado": resultado})

        elif tool_name == "buscar_por_proveedor":
            nombre = arguments.get("nombre", "")
            facturas = Factura.objects.filter(
                proveedor__nombre__icontains=nombre
            ).select_related("proveedor", "categoria").order_by("-fecha_emision")
            resultado = []
            for f in facturas:
                resultado.append({
                    "id": f.id,
                    "numero_factura": f.numero_factura,
                    "proveedor": f.proveedor.nombre,
                    "fecha_emision": f.fecha_emision.isoformat(),
                    "total": float(f.total),
                    "categoria": f.categoria.nombre if f.categoria else None
                })
            return JsonResponse({"resultado": resultado})

        elif tool_name == "resumen_fiscal":
            from django.db.models import Sum
            mes = arguments.get("mes")
            anio = arguments.get("anio")

            # Total de facturas del mes
            facturas_mes = Factura.objects.filter(
                fecha_emision__month=mes,
                fecha_emision__year=anio
            )
            total_facturas = facturas_mes.count()

            # Total IVA soportado
            total_iva = facturas_mes.aggregate(Sum('iva_total'))['iva_total__sum'] or 0

            # Categoría con más gasto
            categoria_top = facturas_mes.filter(
                categoria__isnull=False
            ).values('categoria__nombre').annotate(
                total=Sum('base_imponible')
            ).order_by('-total').first()

            resultado = {
                "mes": mes,
                "anio": anio,
                "total_facturas": total_facturas,
                "total_iva_soportado": float(total_iva),
                "categoria_mas_gasto": categoria_top['categoria__nombre'] if categoria_top else None,
                "gasto_categoria_top": float(categoria_top['total']) if categoria_top else 0
            }
            return JsonResponse({"resultado": resultado})

        else:
            return JsonResponse({"error": f"Herramienta {tool_name} no encontrada"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
