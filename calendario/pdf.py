from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.graphics import renderSVG
from datetime import timedelta

from .fechas import calcular_semanas, formatear_fecha


MARGIN = 50
HEADER_HEIGHT = 20

FONT_HEADER = ("Courier-Bold", 11)
FONT_DAYS = ("Helvetica", 8)

DIAS = [
    "LUNES", "MARTES", "MIÉRCOLES", "JUEVES",
    "VIERNES", "SÁBADO", "DOMINGO"
]


def _calcular_layout(inicio, fin, media_pagina=False):
    """Calcula las dimensiones y posiciones del calendario.

    Retorna un diccionario con todos los parámetros de layout necesarios
    para dibujar el calendario en cualquier formato.
    """
    width, height = A4
    bottom_limit = height / 2 if media_pagina else MARGIN

    usable_width = width - 2 * MARGIN
    usable_height = (height - MARGIN) - bottom_limit
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
    }


def _construir_drawing(inicio, fin, media_pagina=False):
    """Construye un Drawing de ReportLab con el calendario.

    Usado para exportar a SVG y PNG.
    """
    layout = _calcular_layout(inicio, fin, media_pagina)

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

    d = Drawing(width, height)

    # Marco exterior
    d.add(Rect(
        MARGIN, bottom_limit, usable_width, usable_height,
        fillColor=None, strokeColor=None, strokeWidth=1,
    ))
    # Dibujar las 4 líneas del marco manualmente ya que Rect con
    # strokeColor a veces no renderiza bien en SVG
    d.add(Line(MARGIN, bottom_limit, MARGIN + usable_width, bottom_limit))
    d.add(Line(MARGIN, bottom_limit, MARGIN, bottom_limit + usable_height))
    d.add(Line(MARGIN + usable_width, bottom_limit,
               MARGIN + usable_width, bottom_limit + usable_height))
    d.add(Line(MARGIN, bottom_limit + usable_height,
               MARGIN + usable_width, bottom_limit + usable_height))

    # Líneas verticales separadoras de días
    for i in range(1, 7):
        x = MARGIN + i * day_width
        d.add(Line(x, bottom_limit, x, bottom_limit + usable_height))

    # Línea del encabezado
    d.add(Line(MARGIN, header_y, MARGIN + usable_width, header_y))

    # Nombres de los días (encabezado)
    for i, dia in enumerate(DIAS):
        x_center = MARGIN + i * day_width + day_width / 2
        d.add(String(
            x_center, text_y - 3, dia,
            fontName=FONT_HEADER[0],
            fontSize=FONT_HEADER[1],
            textAnchor="middle",
        ))

    # Líneas horizontales separadoras de semanas
    for i in range(1, num_weeks):
        y = header_y - i * week_height
        d.add(Line(MARGIN, y, MARGIN + usable_width, y))

    # Fechas
    for day in range(total_days):
        fecha = start_monday + timedelta(days=day)
        col = day % 7
        row = day // 7

        x = MARGIN + col * day_width + 5
        y = header_y - row * week_height - 12

        texto = formatear_fecha(fecha, start_monday)

        d.add(String(
            x, y, texto,
            fontName=FONT_DAYS[0],
            fontSize=FONT_DAYS[1],
            textAnchor="start",
        ))

    return d


def generar_pdf(nombre_pdf, inicio, fin, media_pagina=False):
    """Genera el calendario en formato PDF usando canvas.Canvas."""

    layout = _calcular_layout(inicio, fin, media_pagina)

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

    c = canvas.Canvas(nombre_pdf, pagesize=A4)

    # marco exterior
    c.rect(MARGIN, bottom_limit, usable_width, usable_height)

    for i in range(1, 7):
        x = MARGIN + i * day_width
        c.line(x, bottom_limit, x, bottom_limit + usable_height)

    # encabezado
    c.line(MARGIN, header_y, MARGIN + usable_width, header_y)

    c.setFont(*FONT_HEADER)

    for i, dia in enumerate(DIAS):

        x_center = MARGIN + i * day_width + day_width / 2
        text_width = c.stringWidth(dia)

        c.drawString(x_center - text_width / 2, text_y - 3, dia)

    # líneas de semana
    for i in range(1, num_weeks):
        y = header_y - i * week_height
        c.line(MARGIN, y, MARGIN + usable_width, y)

    # fechas
    c.setFont(*FONT_DAYS)

    for day in range(total_days):

        fecha = start_monday + timedelta(days=day)

        col = day % 7
        row = day // 7

        x = MARGIN + col * day_width + 5
        y = header_y - row * week_height - 12

        texto = formatear_fecha(fecha, start_monday)

        c.drawString(x, y, texto)

    c.save()


def generar_svg(nombre_svg, inicio, fin, media_pagina=False):
    """Genera el calendario en formato SVG."""
    d = _construir_drawing(inicio, fin, media_pagina)
    renderSVG.drawToFile(d, nombre_svg)


def generar_png(nombre_png, inicio, fin, media_pagina=False):
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

    d = _construir_drawing(inicio, fin, media_pagina)

    try:
        renderPM.drawToFile(d, nombre_png, fmt="PNG")
    except Exception as e:
        raise ImportError(
            "No se pudo generar el PNG. Asegurate de tener 'rlPyCairo' instalado.\n"
            "Instala con: pip install rlPyCairo\n"
            f"Error original: {e}"
        )
