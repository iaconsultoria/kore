from datetime import date
from .models import Cita
from .ia.analizador import analizar_dia


def listar_citas(fecha: str) -> dict:
    fecha_obj = date.fromisoformat(fecha)
    citas = Cita.objects.filter(inicio=fecha_obj).order_by("hora_inicio")
    return {
        "fecha": fecha,
        "citas": [
            {
                "titulo": c.titulo,
                "hora_inicio": str(c.hora_inicio) if c.hora_inicio else None,
                "hora_fin": str(c.hora_fin) if c.hora_fin else None,
                "categoria": c.categoria.nombre if c.categoria else None,
                "prioridad": c.get_prioridad_display(),
            }
            for c in citas
        ]
    }


def detectar_sobrecarga(fecha: str) -> dict:
    fecha_obj = date.fromisoformat(fecha)
    analisis = analizar_dia(fecha_obj)
    return {
        "fecha": fecha,
        "sobrecargado": analisis["sobrecargado"],
        "horas_totales": analisis["horas_totales"],
        "sin_pausa_larga": analisis["sin_pausa_larga"],
    }

def resumen_dia(fecha: str) -> dict:
    citas = listar_citas(fecha)
    sobrecarga = detectar_sobrecarga(fecha)
    n = len(citas["citas"])

    if n == 0:
        texto = "Sin citas, día libre."
    elif sobrecarga["sobrecargado"]:
        texto = f"{n} cita{'s' if n > 1 else ''}, día cargado."
    else:
        texto = f"{n} cita{'s' if n > 1 else ''}, día equilibrado."

    return {
        "fecha": fecha,
        "num_citas": n,
        "sobrecargado": sobrecarga["sobrecargado"],
        "resumen": texto,
    }