from datetime import timedelta

MESES = [
    "enero","febrero","marzo","abril","mayo","junio",
    "julio","agosto","septiembre","octubre","noviembre","diciembre"
]


def calcular_semanas(inicio, fin):

    start_monday = inicio - timedelta(days=inicio.weekday())
    end_sunday = fin + timedelta(days=(6 - fin.weekday()))

    total_days = (end_sunday - start_monday).days + 1
    num_weeks = total_days // 7

    return start_monday, end_sunday, num_weeks


def formatear_fecha(fecha, inicio_calendario):

    dia = fecha.day
    mes = MESES[fecha.month - 1]

    if fecha == inicio_calendario or dia == 1:
        return f"{dia} de {mes}"

    return f"{dia}"

