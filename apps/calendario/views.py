from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from .models import Cita, Categoria
from .forms import CitaForm
from django.conf import settings
from litellm import completion
from .ia.analizador import analizar_dia
from .ia.parser_voz import parsear_texto_a_cita
from .mcp.mcp_server import listar_citas, detectar_sobrecarga, resumen_dia
import requests
import json
import os
import tempfile
from faster_whisper import WhisperModel


from django.middleware.csrf import get_token

def cita_list(request):
    citas = Cita.objects.select_related("categoria").all()
    today = date.today()
    aviso_facturas = None
    try:
        csrftoken = get_token(request)

        session = requests.Session()
        session.cookies.set("csrftoken", csrftoken)

        response = session.post(
            "http://127.0.0.1:8000/facturas/mcp/",
            json={
                "name": "resumen_fiscal",
                "arguments": {
                    "mes": today.month,
                    "anio": today.year,
                }
            },
            headers={
                "Authorization": f"Bearer {settings.FACTURAS_MCP_TOKEN}",
                "X-CSRFToken": csrftoken,
                "Referer": "http://127.0.0.1:8000/",
            },
            timeout=2,
        )
        print("STATUS:", response.status_code)
        if response.status_code == 200:
            data = response.json().get("resultado", {})
            total_facturas = data.get("total_facturas", 0)
            if total_facturas > 0:
                aviso_facturas = f"Este mes hay {total_facturas} factura{'s' if total_facturas > 1 else ''} registrada{'s' if total_facturas > 1 else ''}."
    except Exception as e:
        print("ERROR FACTURAS MCP:", e)
    return render(request, "calendario/cita_list.html", {
        "citas": citas,
        "aviso_facturas": aviso_facturas,
        "today": today.isoformat(),
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
            response["HX-Retarget"] = "#cita-list"
            response["HX-Reswap"] = "beforeend"
            return response
        else:
            response = render(request, "calendario/partials/cita_form.html", {"form": form, "today": date.today().isoformat()})
            response["HX-Retarget"] = "#form-container"
            response["HX-Reswap"] = "innerHTML"
            return response
    return render(request, "calendario/partials/cita_form.html", {"form": form, "today": date.today().isoformat()})


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
        "anotaciones": resultado.get("anotaciones", ""),
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
    return HttpResponse("")


def sugerir_reprogramacion(request, fecha_str):
    fecha = date.fromisoformat(fecha_str)
    analisis = analizar_dia(fecha)

    if not analisis["sobrecargado"]:
        return render(request, "calendario/sugerencia.html", {
            "fecha": fecha,
            "equilibrado": True,
        })

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
    cita.inicio = cita.inicio + timedelta(days=1)
    cita.fin = cita.fin + timedelta(days=1)
    cita.save()
    return HttpResponse("")


def transcribir(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    audio = request.FILES.get("audio")
    if not audio:
        return JsonResponse(
            {"error": "No se ha recibido audio, inténtalo de nuevo."},
            status=400,
        )

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        for chunk in audio.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(tmp_path, language="es")
        texto = " ".join([s.text.strip() for s in segments]).strip()

        if not texto:
            return JsonResponse(
                {"error": "No se ha entendido el audio, inténtalo de nuevo."},
                status=400,
            )

        return JsonResponse({"texto": texto})

    except Exception:
        return JsonResponse(
            {"error": "No se ha entendido el audio, inténtalo de nuevo."},
            status=400,
        )

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


@csrf_exempt
def mcp(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    # Verificar token Bearer
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {settings.MCP_SECRET_TOKEN}":
        return JsonResponse({"error": "No autorizado"}, status=403)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Cuerpo JSON inválido"}, status=400)

    herramienta = body.get("tool")
    params = body.get("params", {})
    fecha = params.get("fecha")

    if not fecha:
        return JsonResponse({"error": "El parámetro 'fecha' es obligatorio"}, status=400)

    try:
        date.fromisoformat(fecha)
    except ValueError:
        return JsonResponse(
            {"error": f"Formato de fecha inválido: '{fecha}'. Usa YYYY-MM-DD"},
            status=400,
        )

    if herramienta == "listar_citas":
        resultado = listar_citas(fecha)
    elif herramienta == "detectar_sobrecarga":
        resultado = detectar_sobrecarga(fecha)
    elif herramienta == "resumen_dia":
        resultado = resumen_dia(fecha)
    else:
        return JsonResponse(
            {"error": f"Herramienta '{herramienta}' no encontrada"},
            status=404,
        )

    return JsonResponse(resultado)