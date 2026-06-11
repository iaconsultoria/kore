from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Factura, LineaFactura, CategoriaGasto, SugerenciaCategoria
from .forms import RevisionFacturaForm
from .utils import buscar_normativa_por_texto, sugerir_categoria, obtener_citas_del_mismo_dia
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

def rate_limit_mcp(view_func):
    """Rate limit: 30 llamadas por minuto por token."""
    def wrapper(request, *args, **kwargs):
        token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token_enviado:
            token_enviado = 'sin-token'

        cache_key = f"mcp_calls_{token_enviado}"
        llamadas = cache.get(cache_key, [])

        ahora = timezone.now().timestamp()
        hace_un_minuto = ahora - 60

        # Limpia llamadas de hace más de 1 minuto
        llamadas = [t for t in llamadas if t > hace_un_minuto]

        if len(llamadas) >= 30:
            return JsonResponse({"error": "Demasiadas solicitudes. Límite: 30 por minuto."}, status=429)

        llamadas.append(ahora)
        cache.set(cache_key, llamadas, 60)

        return view_func(request, *args, **kwargs)
    return wrapper

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

    # Buscar citas del mismo día en calendario
    citas_coincidentes = obtener_citas_del_mismo_dia(factura.fecha_emision)

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
        'fragmentos_normativa': fragmentos_normativa,
        'citas_coincidentes': citas_coincidentes
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
    from datetime import date

    hoy = timezone.now().date()

    # Mes actual
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Mes anterior
    if mes_actual == 1:
        mes_anterior = 12
        anio_anterior = anio_actual - 1
    else:
        mes_anterior = mes_actual - 1
        anio_anterior = anio_actual

    # IVA soportado mes actual
    lineas_mes = LineaFactura.objects.filter(
        factura__fecha_emision__month=mes_actual,
        factura__fecha_emision__year=anio_actual
    )
    iva_mes = sum(
        (linea.precio_unitario * linea.cantidad * linea.iva_porcentaje / 100)
        for linea in lineas_mes
    )

    # Gastos por categoría mes actual
    gastos_por_categoria = Factura.objects.filter(
        categoria__isnull=False,
        fecha_emision__month=mes_actual,
        fecha_emision__year=anio_actual
    ).values('categoria__nombre').annotate(
        total=Sum('base_imponible')
    ).order_by('-total')

    # Total gasto mes actual
    total_mes_actual = sum(cat['total'] for cat in gastos_por_categoria) or 0

    # Total gasto mes anterior
    total_mes_anterior = Factura.objects.filter(
        fecha_emision__month=mes_anterior,
        fecha_emision__year=anio_anterior
    ).aggregate(total=Sum('base_imponible'))['total'] or 0

    # Facturas sin clasificar
    sin_clasificar = Factura.objects.filter(
        categoria__isnull=True,
        fecha_emision__month=mes_actual,
        fecha_emision__year=anio_actual
    ).count()

    # Datos para gráfico (nombres y totales)
    categorias_nombres = [cat['categoria__nombre'] for cat in gastos_por_categoria]
    categorias_totales = [float(cat['total']) for cat in gastos_por_categoria]

    return render(request, 'facturas/dashboard_fiscal.html', {
        'iva_mes': iva_mes,
        'gastos_por_categoria': gastos_por_categoria,
        'sin_clasificar': sin_clasificar,
        'total_mes_actual': total_mes_actual,
        'total_mes_anterior': total_mes_anterior,
        'categorias_nombres': categorias_nombres,
        'categorias_totales': categorias_totales,
        'mes_actual': mes_actual,
        'anio_actual': anio_actual,
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
        return HttpResponse(f"<p>Error al sugerir categoría. Intenta de nuevo más tarde.</p>")

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


def validar_parametros(tool_name, arguments):
    """Valida parámetros según la herramienta."""
    errores = []

    if tool_name == "listar_facturas":
        limit = arguments.get("limit", 10)
        offset = arguments.get("offset", 0)
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            errores.append("limit debe ser un entero entre 1 y 100")
        if not isinstance(offset, int) or offset < 0:
            errores.append("offset debe ser un entero >= 0")

    elif tool_name == "buscar_por_proveedor":
        nombre = arguments.get("nombre")
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) == 0:
            errores.append("nombre debe ser una cadena no vacía")

        fecha_desde = arguments.get("fecha_desde")
        if fecha_desde and not isinstance(fecha_desde, str):
            errores.append("fecha_desde debe ser string formato YYYY-MM-DD")

        fecha_hasta = arguments.get("fecha_hasta")
        if fecha_hasta and not isinstance(fecha_hasta, str):
            errores.append("fecha_hasta debe ser string formato YYYY-MM-DD")

        total_minimo = arguments.get("total_minimo")
        if total_minimo is not None and not isinstance(total_minimo, (int, float)):
            errores.append("total_minimo debe ser un número")

        total_maximo = arguments.get("total_maximo")
        if total_maximo is not None and not isinstance(total_maximo, (int, float)):
            errores.append("total_maximo debe ser un número")

        categoria = arguments.get("categoria")
        if categoria and not isinstance(categoria, str):
            errores.append("categoria debe ser string")

    elif tool_name == "obtener_factura":
        id_factura = arguments.get("id")
        if not isinstance(id_factura, int) or id_factura < 1:
            errores.append("id debe ser un entero > 0")

    elif tool_name == "resumen_fiscal":
        mes = arguments.get("mes")
        anio = arguments.get("anio")
        if not isinstance(mes, int) or mes < 1 or mes > 12:
            errores.append("mes debe ser un entero entre 1 y 12")
        if not isinstance(anio, int) or anio < 1950 or anio > 2100:
            errores.append("anio debe ser un entero entre 1950 y 2100")

    return errores

@rate_limit_mcp
@csrf_exempt
@require_http_methods(["POST"])
def mcp_endpoint(request):
    """Endpoint MCP que maneja llamadas a herramientas."""
    # Validar token
    from django.conf import settings
    import os

    token_esperado = os.getenv('FACTURAS_MCP_TOKEN')
    token_enviado = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not token_esperado or token_enviado != token_esperado:
        return JsonResponse({"error": "No autorizado"}, status=401)

    try:
        body = json.loads(request.body)
        tool_name = body.get("name")
        arguments = body.get("arguments", {})

        # Validar parámetros
        errores = validar_parametros(tool_name, arguments)
        if errores:
            return JsonResponse({"error": ", ".join(errores)}, status=400)

        if tool_name == "listar_facturas":
            limit = arguments.get("limit", 10)
            offset = arguments.get("offset", 0)
            facturas = Factura.objects.select_related("proveedor", "categoria").order_by("-fecha_emision")[offset:offset+limit]
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
            fecha_desde = arguments.get("fecha_desde")
            fecha_hasta = arguments.get("fecha_hasta")
            total_minimo = arguments.get("total_minimo")
            total_maximo = arguments.get("total_maximo")
            categoria = arguments.get("categoria")

            query = Factura.objects.filter(
                proveedor__nombre__icontains=nombre
            )

            if fecha_desde:
                query = query.filter(fecha_emision__gte=fecha_desde)
            if fecha_hasta:
                query = query.filter(fecha_emision__lte=fecha_hasta)
            if total_minimo is not None:
                query = query.filter(total__gte=total_minimo)
            if total_maximo is not None:
                query = query.filter(total__lte=total_maximo)
            if categoria:
                query = query.filter(categoria__nombre__icontains=categoria)

            facturas = query.select_related("proveedor", "categoria").order_by("-fecha_emision")
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

        elif tool_name == "obtener_factura":
            id_factura = arguments.get("id")
            try:
                factura = Factura.objects.get(pk=id_factura)
                lineas = factura.lineafactura_set.all()

                resultado = {
                    "id": factura.id,
                    "numero_factura": factura.numero_factura,
                    "proveedor": factura.proveedor.nombre,
                    "fecha_emision": factura.fecha_emision.isoformat(),
                    "fecha_vencimiento": factura.fecha_vencimiento.isoformat() if factura.fecha_vencimiento else None,
                    "base_imponible": float(factura.base_imponible),
                    "iva_total": float(factura.iva_total),
                    "total": float(factura.total),
                    "categoria": factura.categoria.nombre if factura.categoria else None,
                    "lineas": [
                        {
                            "concepto": linea.concepto,
                            "cantidad": float(linea.cantidad),
                            "precio_unitario": float(linea.precio_unitario),
                            "iva_porcentaje": linea.iva_porcentaje
                        }
                        for linea in lineas
                    ]
                }
                return JsonResponse({"resultado": resultado})
            except Factura.DoesNotExist:
                return JsonResponse({"error": "Factura no encontrada"}, status=404)

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
        return JsonResponse({"error": "Error interno del servidor. Contacta con soporte."}, status=500)


def exportar_dashboard_pdf(request):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from django.db.models import Sum
    from datetime import date
    import io

    hoy = timezone.now().date()
    mes_actual = hoy.month
    anio_actual = hoy.year

    if mes_actual == 1:
        mes_anterior = 12
        anio_anterior = anio_actual - 1
    else:
        mes_anterior = mes_actual - 1
        anio_anterior = anio_actual

    # Datos
    lineas_mes = LineaFactura.objects.filter(
        factura__fecha_emision__month=mes_actual,
        factura__fecha_emision__year=anio_actual
    )
    iva_mes = sum(
        linea.precio_unitario * linea.cantidad * linea.iva_porcentaje / 100
        for linea in lineas_mes
    )

    gastos_por_categoria = Factura.objects.filter(
        categoria__isnull=False,
        fecha_emision__month=mes_actual,
        fecha_emision__year=anio_actual
    ).values('categoria__nombre').annotate(
        total=Sum('base_imponible')
    ).order_by('-total')

    total_mes_actual = sum(cat['total'] for cat in gastos_por_categoria) or 0

    total_mes_anterior = Factura.objects.filter(
        fecha_emision__month=mes_anterior,
        fecha_emision__year=anio_anterior
    ).aggregate(total=Sum('base_imponible'))['total'] or 0

    sin_clasificar = Factura.objects.filter(
        categoria__isnull=True,
        fecha_emision__month=mes_actual,
        fecha_emision__year=anio_actual
    ).count()

    # PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Resumen Fiscal Mensual — Kore", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Fecha de generación: {hoy.strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Paragraph(f"Período: {mes_actual}/{anio_actual}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Totales", styles['Heading2']))
    elements.append(Spacer(1, 8))

    resumen = [
        ['Concepto', 'Importe'],
        ['IVA soportado (mes)', f"{iva_mes:.2f} €"],
        ['Gasto total mes actual', f"{total_mes_actual:.2f} €"],
        ['Gasto total mes anterior', f"{total_mes_anterior:.2f} €"],
        ['Facturas sin clasificar', str(sin_clasificar)],
    ]
    t = Table(resumen, colWidths=[300, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Gastos por categoría", styles['Heading2']))
    elements.append(Spacer(1, 8))

    if gastos_por_categoria:
        datos_cat = [['Categoría', 'Base imponible']]
        for g in gastos_por_categoria:
            datos_cat.append([g['categoria__nombre'], f"{g['total']:.2f} €"])
        tc = Table(datos_cat, colWidths=[300, 150])
        tc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(tc)
    else:
        elements.append(Paragraph("No hay gastos clasificados este mes.", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="dashboard_fiscal_{mes_actual}_{anio_actual}.pdf"'
    })
