from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import Base

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)
    cif = Column(String, unique=True)
    iva = Column(Float)
    descuento = Column(Float)


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    color = Column(String)
    referencia = Column(String, unique=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"))
    ubicacion = Column(String)
    imagen = Column(String)


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, nullable=False)
    fecha_pedido = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    estado = Column(String, nullable=False)


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)


class Cliente(Base):
    __tablename__ = "clientes"

    ADMIN = 0
    CLIENTE = 1

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String)
    direccion = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(Integer, nullable=False, default=CLIENTE)