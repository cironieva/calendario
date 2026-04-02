#!/usr/bin/env python3

import os
import argparse
from datetime import datetime

from .pdf import generar_pdf, generar_svg, generar_png
from . import __version__

FORMATOS_EXTENSION = {
    "pdf": ".pdf",
    "svg": ".svg",
    "png": ".png",
}


def obtener_nombre_archivo(extension=".pdf"):

    contador = 1

    while True:

        nombre = f"calendario-{contador:02d}{extension}"

        if not os.path.exists(nombre):
            return nombre

        contador += 1


def parsear_argumentos():

    parser = argparse.ArgumentParser(
        prog="calendario",
        description="Genera un calendario en PDF, SVG o PNG entre dos fechas."
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
        help="generar calendario de media página"
    )

    parser.add_argument(
        "--formato",
        choices=["pdf", "png", "svg"],
        default="pdf",
        help="formato de salida (default: pdf)"
    )

    return parser.parse_args()


GENERADORES = {
    "pdf": generar_pdf,
    "svg": generar_svg,
    "png": generar_png,
}


def main():

    args = parsear_argumentos()

    try:
        inicio = datetime.strptime(args.inicio, "%d-%m-%Y")
        fin = datetime.strptime(args.fin, "%d-%m-%Y")
    except ValueError:
        print("Error: formato de fecha inválido. Usa DD-MM-AAAA")
        return

    if inicio > fin:
        print("Error: la fecha de inicio no puede ser mayor que la fecha final.")
        return

    extension = FORMATOS_EXTENSION[args.formato]
    nombre_archivo = obtener_nombre_archivo(extension)

    generador = GENERADORES[args.formato]

    try:
        generador(nombre_archivo, inicio, fin, media_pagina=args.media)
    except ImportError as e:
        print(f"Error: {e}")
        return

    print(f"Calendario creado: {nombre_archivo}")


if __name__ == "__main__":
    main()
