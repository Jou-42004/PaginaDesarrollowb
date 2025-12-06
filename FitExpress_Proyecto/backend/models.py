from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    rut = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    comuna = Column(String)
    region = Column(String)
    rol = Column(String, default="cliente")
    
    carrito = relationship("Carrito", back_populates="usuario", uselist=False)
    pedidos = relationship("Pedido", back_populates="usuario")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio_base = Column(Integer)
    imagen_url = Column(String)
    descripcion = Column(String)
    tipo = Column(String)
    kcal = Column(Integer)
    proteina = Column(Float)
    grasas = Column(Float)
    carbs = Column(Float)
    disponible = Column(Boolean, default=True)

class Carrito(Base):
    __tablename__ = "carritos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="carrito")
    items = relationship("CarritoItem", back_populates="carrito", cascade="all, delete-orphan")

class CarritoItem(Base):
    __tablename__ = "carrito_items"
    id = Column(Integer, primary_key=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carritos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=1)
    personalizacion = Column(Text, nullable=True)
    # NUEVO CAMPO: Para guardar el precio calculado con extras
    precio_guardado = Column(Integer, nullable=True) 
    
    carrito = relationship("Carrito", back_populates="items")
    producto = relationship("Producto")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_creacion = Column(DateTime, default=datetime.now)
    total = Column(Integer)
    estado = Column(String, default="Recibido") 
    direccion_envio = Column(String)
    metodo_pago = Column(String)
    repartidor = Column(String, nullable=True)
    
    usuario = relationship("Usuario", back_populates="pedidos")
    items = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "items_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    nombre_producto = Column(String)
    precio_unitario = Column(Integer)
    cantidad = Column(Integer)
    personalizacion = Column(Text, nullable=True)
    
    pedido = relationship("Pedido", back_populates="items")