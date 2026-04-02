from __future__ import annotations

from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderSVG
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.pdfgen import canvas

from .fechas import calcular_semanas, formatear_fecha


HEADER_HEIGHT = 20

FONT_HEADER = ("Courier-Bold", 11)
FONT_EVENTO = ("Helvetica", 6)

CELL_TEXT_OFFSET_X = 5
CELL_TEXT_OFFSET_Y = 12
HEADER_TEXT_OFFSET_Y = 3

COLOR_EVENTO = colors.HexColor("#cc0000")

DIAS = [
    "LUNES", "MARTES", "MIERCOLES", "JUEVES",
    "VIERNES", "SABADO", "DOMINGO",
]


def _calcular_layout(
    inicio: date, fin: date, media_pagina: bool = False, margin: int = 50,
) -> dict:
    """Calcula las dimensiones y posiciones del calendario."""
    width, height = A4
    bottom_limit = height / 2 if media_pagina else margin

    usable_width = width - 2 * margin
    usable_height = (height - margin) - bottom_limit
    day_width = usable_width / 7

    header_y = bottom_limit + usable_height - HEADER_HEIGHT
    text_y = header_y + HEADER_HEIGHT / 2

    start_monday, end_sunday, num_weeks = calcular_semanas(inicio, fin)

    weeks_area_height = header_y - bottom_limit
    week_height = weeks_area_height / num_weeks

    total_days = (end_sunday - start_monday).days + 1

    return {
        "width": width,
        "height": height,
        "bottom_limit": bottom_limit,
        "usable_width": usable_width,
        "usable_height": usable_height,
        "day_width": day_width,
        "header_y": header_y,
        "text_y": text_y,
        "start_monday": start_monday,
        "end_sunday": end_sunday,
        "num_weeks": num_weeks,
        "weeks_area_height": weeks_area_height,
        "week_height": week_height,
        "total_days": total_days,
        "margin": margin,
    }


def _construir_drawing(
    inicio: date, fin: date, media_pagina: bool = False,
    margin: int = 50, font: str = "Helvetica", font_size: int = 8,
) -> Drawing:
    """Construye un Drawing de ReportLab con el calendario.

    Usado para exportar a SVG y PNG.
    """
    layout = _calcular_layout(inicio, fin, media_pagina, margin)

    width = layout["width"]
    height = layout["height"]
    bottom_limit = layout["bottom_limit"]
    usable_width = layout["usable_width"]
    usable_height = layout["usable_height"]
    day_width = layout["day_width"]
    header_y = layout["header_y"]
    text_y = layout["text_y"]
    start_monday = layout["start_monday"]
    num_weeks = layout["num_weeks"]
    week_height = layout["week_height"]
    total_days = layout["total_days"]
    m = layout["margin"]

    d = Drawing(width, height)

    # Marco exterior
    d.add(Line(m, bottom_limit, m + usable_width, bottom_limit))
    d.add(Line(m, bottom_limit, m, bottom_limit + usable_height))
    d.add(Line(m + usable_width, bottom_limit,
               m + usable_width, bottom_limit + usable_height))
    d.add(Line(m, bottom_limit + usable_height,
               m + usable_width, bottom_limit + usable_height))

    # Líneas verticales separadoras de días
    for i in range(1, 7):
        x = m + i * day_width
        d.add(Line(x, bottom_limit, x, bottom_limit + usable_height))

    # Línea del encabezado
    d.add(Line(m, header_y, m + usable_width, header_y))

    # Nombres de los días (encabezado)
    for i, dia in enumerate(DIAS):
        x_center = m + i * day_width + day_width / 2
        d.add(String(
            x_center, text_y - HEADER_TEXT_OFFSET_Y, dia,
            fontName=FONT_HEADER[0],
            fontSize=FONT_HEADER[1],
            textAnchor="middle",
        ))

    # Líneas horizontales separadoras de semanas
    for i in range(1, num_weeks):
        y = header_y - i * week_height
        d.add(Line(m, y, m + usable_width, y))

    # Fechas
    for day in range(total_days):
        fecha = start_monday + timedelta(days=day)
        col = day % 7
        row = day // 7

        x = m + col * day_width + CELL_TEXT_OFFSET_X
        y = header_y - row * week_height - CELL_TEXT_OFFSET_Y

        texto = formatear_fecha(fecha, start_monday)

        d.add(String(
            x, y, texto,
            fontName=font,
            fontSize=font_size,
            textAnchor="start",
        ))

    return d


def generar_pdf(
    nombre_pdf: str, inicio: date, fin: date, media_pagina: bool = False,
    color: str = "#000000", font: str = "Helvetica", margin: int = 50, font_size: int = 8,
    eventos: dict | None = None,
) -> None:

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

        c.drawString(x_center - text_width / 2, text_y - HEADER_TEXT_OFFSET_Y, dia)

    # calculo de semanas
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

        x = margin + col * day_width + CELL_TEXT_OFFSET_X
        y = header_y - row * week_height - CELL_TEXT_OFFSET_Y

        texto = formatear_fecha(fecha, start_monday)

        fecha_date = fecha.date() if hasattr(fecha, "date") else fecha
        es_evento = eventos and fecha_date in eventos

        if es_evento:
            c.setFillColor(COLOR_EVENTO)

        c.drawString(x, y, texto)

        if es_evento:
            c.setFont(*FONT_EVENTO)
            c.drawString(x, y - 8, eventos[fecha_date])
            c.setFont(*font_days)
            c.setFillColor(hex_color)

    c.save()


def generar_svg(
    nombre_svg: str, inicio: date, fin: date, media_pagina: bool = False,
    color: str = "#000000", font: str = "Helvetica", margin: int = 50, font_size: int = 8,
    eventos: dict | None = None,
) -> None:
    """Genera el calendario en formato SVG."""
    d = _construir_drawing(inicio, fin, media_pagina, margin, font, font_size)
    renderSVG.drawToFile(d, nombre_svg)


def generar_png(
    nombre_png: str, inicio: date, fin: date, media_pagina: bool = False,
    color: str = "#000000", font: str = "Helvetica", margin: int = 50, font_size: int = 8,
    eventos: dict | None = None,
) -> None:
    """Genera el calendario en formato PNG.

    Requiere que el paquete 'rlPyCairo' esté instalado.
    """
    try:
        from reportlab.graphics import renderPM
    except ImportError:
        raise ImportError(
            "Para exportar a PNG se necesita instalar 'rlPyCairo'.\n"
            "Instala con: pip install rlPyCairo"
        )

    d = _construir_drawing(inicio, fin, media_pagina, margin, font, font_size)

    try:
        renderPM.drawToFile(d, nombre_png, fmt="PNG")
    except Exception as e:
        raise ImportError(
            "No se pudo generar el PNG. Asegurate de tener 'rlPyCairo' instalado.\n"
            "Instala con: pip install rlPyCairo\n"
            f"Error original: {e}"
        )
