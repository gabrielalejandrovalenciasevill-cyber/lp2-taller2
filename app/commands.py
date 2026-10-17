"""
Comandos personalizados de terminal (Flask CLI).

Permiten ejecutar tareas administrativas desde la terminal, por ejemplo:

    flask init-db     -> crea las tablas en la base de datos
    flask seed-db     -> carga los productos del JSON a la base de datos

Estos comandos se registran en create_app().
"""

import json
import os

import click

from .extensions import db
from .models import Categoria, Producto


RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), "data", "productos.json")
     os.path.dirname(__file__), "data", "productos.json"
) 

def registrar_comandos(app):
    """Asocia los comandos a la aplicación Flask recibida."""

    @app.cli.command("init-db")
    def init_db():
        """Crea todas las tablas definidas en models.py."""
        db.create_all()
        click.echo("Base de datos creada correctamente.")

    @app.cli.command("reset-db")
    def reset_db():
        """Borra y vuelve a crear todas las tablas."""
        db.drop_all()
        db.create_all()
        click.echo("Base de datos reiniciada correctamente.")

    @app.cli.command("seed-db")
    def seed_db():
        """Carga los productos de productos.json en la base de datos."""

        # Leer los productos del archivo JSON
        with open(RUTA_PRODUCTOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        productos_cargados = 0

        # Insertar categorías y productos
        for item in datos:
            categoria = Categoria.query.filter_by(
                nombre=item["categoria"]
            ).first()

            if categoria is None:
                categoria = Categoria(nombre=item["categoria"])
                db.session.add(categoria)
                db.session.flush()

            # Evitar productos duplicados usando el SKU
            producto_existente = Producto.query.filter_by(
                sku=item["sku"]
            ).first()

            if producto_existente is not None:
                continue

            # Crear el producto y relacionarlo con su categoría
            producto = Producto(
                sku=item["sku"],
                marca=item["marca"],
                nombre=item["nombre"],
                precio=item["precio"],
                foto=item.get("foto"),
                stock=item["stock"],
                activo=item.get("activo", True),
                categoria_id=categoria.id
            )

            db.session.add(producto)
            productos_cargados += 1

        # Guardar los cambios en la base de datos
        db.session.commit()

        click.echo(
            f"Se cargaron {productos_cargados} productos correctamente."
        )

