#!/usr/bin/env python3

import os
import json
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
        "--eventos",
        help="ruta a un archivo JSON con eventos especiales"
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

    eventos = None
    if args.eventos:
        try:
            with open(args.eventos, encoding="utf-8") as f:
                datos = json.load(f)
            eventos = {}
            for item in datos:
                fecha = datetime.strptime(item["fecha"], "%d-%m-%Y").date()
                eventos[fecha] = item["nombre"]
        except FileNotFoundError:
            print(f"Error: no se encontró el archivo de eventos: {args.eventos}")
            return
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error al leer el archivo de eventos: {e}")
            return

    nombre_pdf = obtener_nombre_archivo()

    generar_pdf(
        nombre_pdf,
        inicio,
        fin,
        media_pagina=args.media,
        eventos=eventos
    )

    print(f"Calendario creado: {nombre_pdf}")


if __name__ == "__main__":
    main()
