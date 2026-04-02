from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import timedelta

from .fechas import calcular_semanas, formatear_fecha


MARGIN = 50
HEADER_HEIGHT = 20

FONT_HEADER = ("Courier-Bold", 11)
FONT_DAYS = ("Helvetica", 8)
FONT_EVENTO = ("Helvetica", 6)

COLOR_EVENTO = colors.HexColor("#cc0000")

DIAS = [
    "LUNES", "MARTES", "MIÉRCOLES", "JUEVES",
    "VIERNES", "SÁBADO", "DOMINGO"
]


def generar_pdf(nombre_pdf, inicio, fin, media_pagina=False, eventos=None):

    width, height = A4
    bottom_limit = height / 2 if media_pagina else MARGIN

    c = canvas.Canvas(nombre_pdf, pagesize=A4)

    usable_width = width - 2 * MARGIN
    usable_height = (height - MARGIN) - bottom_limit

    # marco exterior
    c.rect(MARGIN, bottom_limit, usable_width, usable_height)

    day_width = usable_width / 7

    for i in range(1, 7):
        x = MARGIN + i * day_width
        c.line(x, bottom_limit, x, bottom_limit + usable_height)

    # encabezado
    header_y = bottom_limit + usable_height - HEADER_HEIGHT
    c.line(MARGIN, header_y, MARGIN + usable_width, header_y)

    c.setFont(*FONT_HEADER)

    text_y = header_y + HEADER_HEIGHT / 2

    for i, dia in enumerate(DIAS):

        x_center = MARGIN + i * day_width + day_width / 2
        text_width = c.stringWidth(dia)

        c.drawString(x_center - text_width / 2, text_y - 3, dia)

    # cálculo de semanas
    start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)

    weeks_area_height = header_y - bottom_limit
    week_height = weeks_area_height / num_weeks

    for i in range(1, num_weeks):
        y = header_y - i * week_height
        c.line(MARGIN, y, MARGIN + usable_width, y)

    # fechas
    total_days = (end_sunday - start_monday).days + 1

    c.setFont(*FONT_DAYS)

    for day in range(total_days):

        fecha = start_monday + timedelta(days=day)

        col = day % 7
        row = day // 7

        x = MARGIN + col * day_width + 5
        y = header_y - row * week_height - 12

        texto = formatear_fecha(fecha, start_monday)

        fecha_date = fecha.date() if hasattr(fecha, "date") else fecha
        es_evento = eventos and fecha_date in eventos

        if es_evento:
            c.setFillColor(COLOR_EVENTO)

        c.drawString(x, y, texto)

        if es_evento:
            c.setFont(*FONT_EVENTO)
            c.drawString(x, y - 8, eventos[fecha_date])
            c.setFont(*FONT_DAYS)
            c.setFillColor(colors.black)

    c.save()
