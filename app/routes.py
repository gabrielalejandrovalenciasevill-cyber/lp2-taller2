"""
Rutas (vistas) de la Tienda Virtual.

CAMBIO CLAVE respecto al Taller 1:
ya NO leemos productos.json en cada petición. Ahora consultamos la base de
datos a través del ORM. Las funciones cargar_productos() y
buscar_producto_por_sku() desaparecen y se reemplazan por consultas
SQLAlchemy como Producto.query.all() o Producto.query.filter_by(...).
"""

from flask import Blueprint, render_template, abort, request

from .models import Producto, Categoria

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Página principal: catálogo de productos desde la base de datos.

   # TODO 1: Leer el filtro opcional de categoría.
    categoria_id = request.args.get("categoria", type=int)

    # Consultar productos según la categoría seleccionada.
    if categoria_id is not None:
        productos = Producto.query.filter_by(
            categoria_id=categoria_id
        ).all()
    else:
        productos = Producto.query.all()

    # TODO 2: Consultar todas las categorías ordenadas por nombre.
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    # TODO 3: Mostrar el catálogo y enviar los datos al HTML.
    return render_template(
        "index.html",
        productos=productos,
        categorias=categorias,
        categoria_id=categoria_id
    )


@main.route("/producto/<sku>")
def detalle(sku):
    """Mostrar el detalle de un producto mediante su SKU."""

    # TODO 4: Buscar el producto por su SKU.
    producto = Producto.query.filter_by(sku=sku).first_or_404()

    # TODO 5: Mostrar la página de detalle.
    return render_template("detalle.html", producto=producto)


@main.route("/categorias")
def categorias():
    """Mostrar las categorías y sus productos."""

    # TODO 6: Consultar las categorías ordenadas por nombre.
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    # TODO 7: Mostrar la página de categorías.
    return render_template("categorias.html", categorias=categorias)