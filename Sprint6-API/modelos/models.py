# ARCHIVO: modelos/models.py

from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import List, Optional
from enum import Enum as PyEnum
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import EmailStr

# --- Enums ---
class EstadoUsuarioEnum(str, PyEnum):
    ACTIVO = "Activo"
    PENDIENTE = "Pendiente"

class EstadoPagoEnum(str, PyEnum):
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    REEMBOLSADO = "reembolsado"

class PrioridadPromocionEnum(str, PyEnum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

# --- Tablas de Enlace ---
class BowlExtraLink(SQLModel, table=True):
    bowl_personalizado_id: Optional[UUID] = Field(default=None, foreign_key="bowlpersonalizado.id", primary_key=True)
    extra_id: Optional[UUID] = Field(default=None, foreign_key="extra.id", primary_key=True)

# --- 1. Usuarios ---
class Usuario(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    nombre: str
    rut: str = Field(unique=True, index=True)
    correo: EmailStr = Field(unique=True, index=True)
    contrasena_hash: str
    telefono: str
    estado: EstadoUsuarioEnum = Field(default=EstadoUsuarioEnum.PENDIENTE)

    historial_contrasena: Optional["HistorialContrasena"] = Relationship(back_populates="usuario")
    token_verificacion: Optional["TokenVerificacion"] = Relationship(back_populates="usuario")
    direcciones: List["Direccion"] = Relationship(back_populates="usuario")
    carrito: Optional["Carrito"] = Relationship(back_populates="usuario")
    pedidos: List["Pedido"] = Relationship(back_populates="usuario")
    datos_facturacion: Optional["DatosFacturacion"] = Relationship(back_populates="usuario")

class HistorialContrasena(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    usuario_id: UUID = Field(foreign_key="usuario.id", unique=True)
    ultimas3: List[str] = Field(sa_column=Column(JSON)) 
    usuario: "Usuario" = Relationship(back_populates="historial_contrasena")

class TokenVerificacion(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    usuario_id: UUID = Field(foreign_key="usuario.id", unique=True)
    codigo: str = Field(index=True)
    expiracion: datetime
    valido: bool = Field(default=True)
    usuario: "Usuario" = Relationship(back_populates="token_verificacion")

# --- 2. Productos ---
class Producto(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    nombre: str
    precio: int
    disponible: bool = Field(default=True)
    imagen_url: str 
    macros_id: UUID = Field(foreign_key="macros.id")

    macros: "Macros" = Relationship()
    items_carrito: List["ItemCarrito"] = Relationship(back_populates="producto")
    items_pedido: List["ItemPedido"] = Relationship(back_populates="producto")

class Macros(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    kcal: int
    p: int
    f: int
    c: int

class TipoBowl(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    esLacteo: bool = Field(default=False)
    maxProteinas: int
    bowls_personalizados: List["BowlPersonalizado"] = Relationship(back_populates="tipo_bowl")

class Extra(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    precio: int
    esLacteo: bool = Field(default=False)
    bowls_personalizados: List["BowlPersonalizado"] = Relationship(back_populates="extras", link_model=BowlExtraLink)

class BowlPersonalizado(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tipo_bowl_id: UUID = Field(foreign_key="tipobowl.id")
    total: int 
    tipo_bowl: "TipoBowl" = Relationship(back_populates="bowls_personalizados")
    items_carrito: List["ItemCarrito"] = Relationship(back_populates="bowl_personalizado")
    items_pedido: List["ItemPedido"] = Relationship(back_populates="bowl_personalizado")
    extras: List["Extra"] = Relationship(back_populates="bowls_personalizados", link_model=BowlExtraLink)

# --- 3. Carrito ---
class Carrito(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    usuario_id: UUID = Field(foreign_key="usuario.id", unique=True, index=True)
    total: int = Field(default=0)
    usuario: "Usuario" = Relationship(back_populates="carrito")
    items: List["ItemCarrito"] = Relationship(back_populates="carrito")

class ItemCarrito(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    carrito_id: UUID = Field(foreign_key="carrito.id")
    cantidad: int
    precio_unitario: int
    producto_id: Optional[UUID] = Field(default=None, foreign_key="producto.id")
    bowl_personalizado_id: Optional[UUID] = Field(default=None, foreign_key="bowlpersonalizado.id")

    carrito: "Carrito" = Relationship(back_populates="items")
    producto: Optional["Producto"] = Relationship(back_populates="items_carrito")
    bowl_personalizado: Optional["BowlPersonalizado"] = Relationship(back_populates="items_carrito")

class Promocion(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str
    prioridad: PrioridadPromocionEnum
    descuento: int
    vigencia_id: UUID = Field(foreign_key="vigencia.id")
    vigencia: "Vigencia" = Relationship()

class Vigencia(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    desde: datetime
    hasta: datetime

# --- 4. Pedidos ---
class Pedido(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    usuario_id: UUID = Field(foreign_key="usuario.id")
    estado_id: UUID = Field(foreign_key="estadopedido.id")
    direccion_id: UUID = Field(foreign_key="direccion.id")
    pago_id: UUID = Field(foreign_key="pago.id")
    descripcion: str
    total: int
    creado_en: datetime = Field(default_factory=datetime.utcnow)

    usuario: "Usuario" = Relationship(back_populates="pedidos")
    estado: "EstadoPedido" = Relationship()
    direccion: "Direccion" = Relationship()
    pago: "Pago" = Relationship(back_populates="pedido")
    items: List["ItemPedido"] = Relationship(back_populates="pedido")

class ItemPedido(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    pedido_id: UUID = Field(foreign_key="pedido.id")
    cantidad: int
    precio_unitario: int
    producto_id: Optional[UUID] = Field(default=None, foreign_key="producto.id")
    bowl_personalizado_id: Optional[UUID] = Field(default=None, foreign_key="bowlpersonalizado.id")
    
    pedido: "Pedido" = Relationship(back_populates="items")
    producto: Optional["Producto"] = Relationship(back_populates="items_pedido")
    bowl_personalizado: Optional["BowlPersonalizado"] = Relationship(back_populates="items_pedido")

class EstadoPedido(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str = Field(unique=True)
    aceptaCancelacion: bool = Field(default=False)

class Pago(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tipo: str
    reembolsable: bool = Field(default=True)
    estado_pago: EstadoPagoEnum = Field(default=EstadoPagoEnum.PENDIENTE)
    pedido: "Pedido" = Relationship(back_populates="pago")

class Comuna(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nombre: str = Field(unique=True)
    tieneCobertura: bool = Field(default=False)
    direcciones: List["Direccion"] = Relationship(back_populates="comuna")

class Direccion(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    usuario_id: UUID = Field(foreign_key="usuario.id")
    comuna_id: UUID = Field(foreign_key="comuna.id")
    calle: str
    numero: str
    depto: Optional[str] = None
    referencia: Optional[str] = None
    favorita: bool = Field(default=False)
    usuario: "Usuario" = Relationship(back_populates="direcciones")
    comuna: "Comuna" = Relationship(back_populates="comuna")

# --- 5. Facturación ---
class DatosFacturacion(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    usuario_id: UUID = Field(foreign_key="usuario.id", unique=True)
    rut_empresa: str = Field(unique=True)
    razon_social: str
    giro: str
    direccion_comercial: str
    comuna: str
    email_dte: EmailStr
    usuario: "Usuario" = Relationship(back_populates="datos_facturacion")