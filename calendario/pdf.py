from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import timedelta

from .fechas import calcular_semanas, formatear_fecha


HEADER_HEIGHT = 20

FONT_HEADER = ("Courier-Bold", 11)

DIAS = [
    "LUNES", "MARTES", "MIÉRCOLES", "JUEVES",
    "VIERNES", "SÁBADO", "DOMINGO"
]


def generar_pdf(nombre_pdf, inicio, fin, media_pagina=False,
                color="#000000", font="Helvetica", margin=50, font_size=8):

    width, height = A4
    bottom_limit = height / 2 if media_pagina else margin

    c = canvas.Canvas(nombre_pdf, pagesize=A4)

    # aplicar color para líneas y texto
    hex_color = colors.HexColor(color)
    c.setStrokeColor(hex_color)
    c.setFillColor(hex_color)

    font_days = (font, font_size)

    usable_width = width - 2 * margin
    usable_height = (height - margin) - bottom_limit

    # marco exterior
    c.rect(margin, bottom_limit, usable_width, usable_height)

    day_width = usable_width / 7

    for i in range(1, 7):
        x = margin + i * day_width
        c.line(x, bottom_limit, x, bottom_limit + usable_height)

    # encabezado
    header_y = bottom_limit + usable_height - HEADER_HEIGHT
    c.line(margin, header_y, margin + usable_width, header_y)

    c.setFont(*FONT_HEADER)

    text_y = header_y + HEADER_HEIGHT / 2

    for i, dia in enumerate(DIAS):

        x_center = margin + i * day_width + day_width / 2
        text_width = c.stringWidth(dia)

        c.drawString(x_center - text_width / 2, text_y - 3, dia)

    # cálculo de semanas
    start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)

    weeks_area_height = header_y - bottom_limit
    week_height = weeks_area_height / num_weeks

    for i in range(1, num_weeks):
        y = header_y - i * week_height
        c.line(margin, y, margin + usable_width, y)

    # fechas
    total_days = (end_sunday - start_monday).days + 1

    c.setFont(*font_days)

    for day in range(total_days):

        fecha = start_monday + timedelta(days=day)

        col = day % 7
        row = day // 7

        x = margin + col * day_width + 5
        y = header_y - row * week_height - 12

        texto = formatear_fecha(fecha, start_monday)

        c.drawString(x, y, texto)

    c.save()

