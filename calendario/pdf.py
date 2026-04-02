from __future__ import annotations

from datetime import date, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .fechas import calcular_semanas, formatear_fecha

MARGIN = 50
HEADER_HEIGHT = 20

FONT_HEADER = ("Courier-Bold", 11)
FONT_DAYS = ("Helvetica", 8)

CELL_TEXT_OFFSET_X = 5
CELL_TEXT_OFFSET_Y = 12
HEADER_TEXT_OFFSET_Y = 3

DIAS = [
    "LUNES", "MARTES", "MIERCOLES", "JUEVES",
    "VIERNES", "SABADO", "DOMINGO",
]


def generar_pdf(
    nombre_pdf: str, inicio: date, fin: date, media_pagina: bool = False
) -> None:

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

        c.drawString(x_center - text_width / 2, text_y - HEADER_TEXT_OFFSET_Y, dia)

    # calculo de semanas
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

        x = MARGIN + col * day_width + CELL_TEXT_OFFSET_X
        y = header_y - row * week_height - CELL_TEXT_OFFSET_Y

        texto = formatear_fecha(fecha, start_monday)

        c.drawString(x, y, texto)

    c.save()
