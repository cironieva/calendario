#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

from . import __version__
from .pdf import generar_pdf, generar_svg, generar_png


FORMATOS_EXTENSION = {
    "pdf": ".pdf",
    "svg": ".svg",
    "png": ".png",
}

GENERADORES = {
    "pdf": generar_pdf,
    "svg": generar_svg,
    "png": generar_png,
}


def obtener_nombre_archivo(extension: str = ".pdf", limite: int = 999) -> str:

    for contador in range(1, limite + 1):

        nombre = f"calendario-{contador:02d}{extension}"

        if not os.path.exists(nombre):
            return nombre

    raise RuntimeError(
        f"No se pudo generar un nombre de archivo disponible "
        f"(se verificaron {limite} nombres)."
    )


def parsear_argumentos() -> argparse.Namespace:

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
        help="generar calendario de media pagina"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="ruta del archivo de salida"
    )

    parser.add_argument(
        "--formato",
        choices=["pdf", "png", "svg"],
        default="pdf",
        help="formato de salida (default: pdf)"
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

    parser.add_argument(
        "--eventos",
        help="ruta a un archivo JSON con eventos especiales"
    )

    return parser.parse_args()


def main() -> None:

    args = parsear_argumentos()

    try:
        inicio = datetime.strptime(args.inicio, "%d-%m-%Y")
        fin = datetime.strptime(args.fin, "%d-%m-%Y")
    except ValueError:
        print("Error: formato de fecha inválido. Usa DD-MM-AAAA")
        sys.exit(1)

    if inicio > fin:
        print("Error: la fecha de inicio no puede ser mayor que la fecha final.")
        sys.exit(1)

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
            sys.exit(1)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error al leer el archivo de eventos: {e}")
            sys.exit(1)

    extension = FORMATOS_EXTENSION[args.formato]
    nombre_archivo = args.output if args.output else obtener_nombre_archivo(extension)

    generador = GENERADORES[args.formato]

    try:
        generador(
            nombre_archivo,
            inicio,
            fin,
            media_pagina=args.media,
            color=args.color,
            font=args.font,
            margin=args.margin,
            font_size=args.font_size,
            eventos=eventos,
        )
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except (OSError, IOError, ValueError, KeyError) as e:
        print(f"Error: no se pudo generar el archivo '{nombre_archivo}': {e}")
        return

    print(f"Calendario creado: {nombre_archivo}")


if __name__ == "__main__":
    main()
