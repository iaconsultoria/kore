from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Cita, Categoria
from .forms import CitaForm


def cita_list(request):
    citas = Cita.objects.select_related("categoria").all()
    return render(request, "calendario/cita_list.html", {"citas": citas})

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
