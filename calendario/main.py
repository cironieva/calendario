#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from datetime import datetime

from . import __version__
from .pdf import generar_pdf


def obtener_nombre_archivo() -> str:

    contador = 1

    while True:

        nombre = f"calendario-{contador:02d}.pdf"

        if not os.path.exists(nombre):
            return nombre

        contador += 1


def parsear_argumentos() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        prog="calendario",
        description="Genera un calendario en PDF entre dos fechas."
    )

    parser.add_argument(
        "inicio",
        help="fecha de inicio (formato: DD-MM-AAAA)"
    )

    parser.add_argument(
        "fin",
        help="fecha de fin (formato: DD-MM-AAAA)"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"calendario {__version__}"
    )

    parser.add_argument(
        "-m",
        "--media",
        action="store_true",
        help="generar calendario de media pagina"
    )

    parser.add_argument(
        "--color",
        default="#000000",
        help="color hexadecimal para lineas y bordes (default: #000000)"
    )

    parser.add_argument(
        "--font",
        default="Helvetica",
        help="nombre de fuente para los numeros de dia (default: Helvetica)"
    )

    parser.add_argument(
        "--margin",
        type=int,
        default=50,
        help="margen en puntos (default: 50)"
    )

    parser.add_argument(
        "--font-size",
        type=int,
        default=8,
        help="tamano de fuente para los numeros de dia (default: 8)"
    )

    return parser.parse_args()


def main() -> None:

    args = parsear_argumentos()

    try:
        inicio = datetime.strptime(args.inicio, "%d-%m-%Y")
        fin = datetime.strptime(args.fin, "%d-%m-%Y")
    except ValueError:
        print("Error: formato de fecha invalido. Usa DD-MM-AAAA")
        return

    if inicio > fin:
        print("Error: la fecha de inicio no puede ser mayor que la fecha final.")
        return

    nombre_pdf = obtener_nombre_archivo()

    try:
        generar_pdf(
            nombre_pdf,
            inicio,
            fin,
            media_pagina=args.media,
            color=args.color,
            font=args.font,
            margin=args.margin,
            font_size=args.font_size,
        )
    except (OSError, IOError) as e:
        print(f"Error: no se pudo generar el archivo '{nombre_pdf}': {e}")
        return

    print(f"Calendario creado: {nombre_pdf}")


if __name__ == "__main__":
    main()
