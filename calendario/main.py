#!/usr/bin/env python3

import os
import argparse
from datetime import datetime

from .pdf import generar_pdf
from . import __version__

def obtener_nombre_archivo():

    contador = 1

    while True:

        nombre = f"calendario-{contador:02d}.pdf"

        if not os.path.exists(nombre):
            return nombre

        contador += 1


def parsear_argumentos():

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
        help="generar calendario de media página"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="ruta del archivo PDF de salida"
    )

    return parser.parse_args()


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

    nombre_pdf = args.output if args.output else obtener_nombre_archivo()

    generar_pdf(
        nombre_pdf,
        inicio,
        fin,
        media_pagina=args.media
    )

    print(f"Calendario creado: {nombre_pdf}")


if __name__ == "__main__":
    main()

