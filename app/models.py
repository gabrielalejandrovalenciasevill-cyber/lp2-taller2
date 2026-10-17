"""
Modelos de datos (ORM SQLAlchemy).

Cada clase que hereda de db.Model representa una TABLA de la base de datos,
y cada atributo db.Column representa una COLUMNA. SQLAlchemy se encarga de
traducir estas clases a SQL y de convertir las filas en objetos Python.
"""

from .extensions import db


class Categoria(db.Model):
    """Categoría a la que pertenece un producto (Periféricos, Audio, etc.)."""

    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)

     # Nombre único y obligatorio de la categoría.
    nombre = db.Column(
        db.String(80),
        nullable=False,
        unique=True
    )

    # Relación uno-a-muchos: una categoría tiene muchos productos.
    productos = db.relationship("Producto", backref="categoria", lazy=True)

    def __repr__(self):
        """Representación legible del objeto (útil al depurar)."""
        return f"<Categoria {self.nombre}>"


class Producto(db.Model):
    """Producto del catálogo de la tienda."""

    __tablename__ = "productos"

    # Clave primaria autoincremental.
    id = db.Column(db.Integer, primary_key=True)

    # Datos del producto.
    sku = db.Column(db.String(20), unique=True, nullable=False)
    marca = db.Column(db.String(80), nullable=False)
    nombre = db.Column(db.String(160), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(200), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    # Llave foránea hacia la tabla categorias.
    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id"),
        nullable=False
    )

    def __repr__(self):
        """Representación legible del producto."""
        return f"<Producto {self.sku} - {self.nombre}>"

    @property
    def disponible(self):
        """True si el producto está activo y tiene unidades en stock."""
        return self.activo and self.stock > 0