from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from datetime import date, datetime
from .models import Cita, Categoria
from .forms import CitaForm
from django.conf import settings
from litellm import completion
from .models import Cita
from .forms import CitaForm
from .ia.analizador import analizar_dia


def cita_list(request):
    citas = Cita.objects.select_related("categoria").all()
    return render(request, "calendario/cita_list.html", {
        "citas": citas,
        "today": date.today().isoformat(),
    })

def cita_boton(request):
    return render(request, "calendario/partials/cita_boton.html")

def cita_create(request):
    form = CitaForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            cita = form.save()
            response = render(request, "calendario/partials/cita_row.html", {"cita": cita})
            response["HX-Trigger"] = "citaGuardada"
            return response
        else:
            response = render(request, "calendario/partials/cita_form.html", {"form": form})
            response["HX-Retarget"] = "#form-container"
            response["HX-Reswap"] = "innerHTML"
            return response
    return render(request, "calendario/partials/cita_form.html", {"form": form})

from django.views.decorators.http import require_POST
from django.shortcuts import render
from .forms import CitaForm
from .ia.parser_voz import parsear_texto_a_cita

@require_POST
def cita_desde_texto(request):
    texto = request.POST.get("texto", "")
    resultado = parsear_texto_a_cita(texto)

    if "clarificacion_necesaria" in resultado:
        return render(request, "calendario/partials/cita_clarificacion.html", {
            "pregunta": resultado["clarificacion_necesaria"]
        })

    form = CitaForm(initial={
        "titulo": resultado.get("titulo", ""),
        "inicio": resultado.get("inicio", ""),
        "hora_inicio": resultado.get("hora_inicio", ""),
        "categoria": resultado.get("categoria_sugerida", ""),
        "notas": resultado.get("notas", ""),
    })

    return render(request, "calendario/partials/cita_form_prerellenado.html", {
        "form": form
    })

def cita_edit(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    form = CitaForm(request.POST or None, instance=cita)
    if request.method == "POST":
        if form.is_valid():
            cita = form.save()
            response = render(request, "calendario/partials/cita_row.html", {"cita": cita})
            response["HX-Retarget"] = f"#cita-{cita.pk}"
            response["HX-Reswap"] = "outerHTML"
            response["HX-Trigger"] = "citaGuardada"
            return response
        else:
            response = render(request, "calendario/partials/cita_form.html", {"form": form, "cita": cita})
            response["HX-Retarget"] = "#form-container"
            response["HX-Reswap"] = "innerHTML"
            return response
    return render(request, "calendario/partials/cita_form.html", {"form": form, "cita": cita})

@require_http_methods(["DELETE"])
def cita_delete(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    cita.delete()
    return HttpResponse("")  # HTMX swap vacío elimina el elemento del DOM

def sugerir_reprogramacion(request, fecha_str):
    fecha = date.fromisoformat(fecha_str)
    analisis = analizar_dia(fecha)
 
    if not analisis["sobrecargado"]:
        return render(request, "calendario/sugerencia.html", {
            "fecha": fecha,
            "equilibrado": True,
        })
 
    # Construir lista de citas para el prompt
    lista_citas = "\n".join([
        f"- {c['titulo']} ({c['hora_inicio'] or 'sin hora'}–{c['hora_fin'] or 'sin hora'})"
        for c in analisis["citas"]
    ])
 
    prompt = (
        f"El usuario tiene estas citas el día {fecha}:\n{lista_citas}\n"
        f"El día está sobrecargado. Sugiere en una frase corta cuál moverías "
        f"y a qué momento del día siguiente. Responde solo con la sugerencia, sin explicaciones."
    )
 
    response = completion(
        model="openrouter/z-ai/glm-4.5-air:free",
        messages=[{"role": "user", "content": prompt}],
        api_key=settings.OPENROUTER_API_KEY,
    )
    sugerencia = response.choices[0].message.content.strip()
 
    # Buscar la cita mencionada en la sugerencia para el botón Aceptar
    citas_del_dia = Cita.objects.filter(inicio=fecha)
    cita_sugerida = None
    for cita in citas_del_dia:
        if cita.titulo.lower() in sugerencia.lower():
            cita_sugerida = cita
            break
 
    return render(request, "calendario/sugerencia.html", {
        "fecha": fecha,
        "equilibrado": False,
        "analisis": analisis,
        "sugerencia": sugerencia,
        "cita_sugerida": cita_sugerida,
    })
 
 
def aceptar_reprogramacion(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    # Mover al día siguiente manteniendo la hora
    from datetime import timedelta
    cita.inicio = cita.inicio + timedelta(days=1)
    cita.fin    = cita.fin + timedelta(days=1)
    cita.save()
    return HttpResponse("")
