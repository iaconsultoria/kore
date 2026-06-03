from datetime import datetime, timedelta, date
from apps.calendario.models import Cita
 
 
def analizar_dia(fecha: date) -> dict:
    citas = list(
        Cita.objects.filter(inicio=fecha)
        .order_by("hora_inicio")
    )
 
    horas_totales = 0.0
 
    for cita in citas:
        if cita.hora_inicio and cita.hora_fin:
            inicio_dt = datetime.combine(fecha, cita.hora_inicio)
            fin_dt    = datetime.combine(fecha, cita.hora_fin)
            duracion  = (fin_dt - inicio_dt).seconds / 3600
        else:
            duracion = 1.0
        horas_totales += duracion
 
    # Detectar si hay alguna pausa > 90 min entre citas consecutivas
    sin_pausa_larga = False
    citas_con_hora  = [c for c in citas if c.hora_inicio and c.hora_fin]
 
    if len(citas_con_hora) > 1:
        hay_pausa_larga = False
        for i in range(len(citas_con_hora) - 1):
            fin_actual      = datetime.combine(fecha, citas_con_hora[i].hora_fin)
            inicio_siguiente = datetime.combine(fecha, citas_con_hora[i + 1].hora_inicio)
            pausa = (inicio_siguiente - fin_actual).seconds / 60
            if pausa > 90:
                hay_pausa_larga = True
                break
        sin_pausa_larga = not hay_pausa_larga
 
    sobrecargado = horas_totales > 6 or sin_pausa_larga
 
    return {
        "sobrecargado":    sobrecargado,
        "horas_totales":   round(horas_totales, 2),
        "sin_pausa_larga": sin_pausa_larga,
        "citas": [
            {
                "titulo":      c.titulo,
                "hora_inicio": str(c.hora_inicio) if c.hora_inicio else None,
                "hora_fin":    str(c.hora_fin)    if c.hora_fin    else None,
            }
            for c in citas
        ],
    }