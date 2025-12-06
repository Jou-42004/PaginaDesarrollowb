from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Optional
from enum import Enum
from datetime import datetime

# --- Enums ---
class EstadoUsuario(str, Enum):
    ACTIVO = "Activo"
    PENDIENTE = "Pendiente"

class EstadoPedido(str, Enum):
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    CANCELADO = "Cancelado"

class PrioridadPromo(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

# --- 1. USUARIOS ---
class Usuario(BaseModel):
    id: UUID4
    nombre: str
    rut: str
    email: EmailStr
    telefono: Optional[str] = None
    estado: EstadoUsuario
    
    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nombre: str
    rut: str
    email: EmailStr
    password: str
    telefono: str
    direccion: str 
    comuna: str
    region: str

class CambioPassword(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str
    confirmar_nueva: str

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario

# --- 2. PRODUCTOS (Debe ir ANTES del carrito) ---
class Macros(BaseModel):
    kcal: int
    p: int
    f: int
    c: int
    
    class Config:
        from_attributes = True

class ProductoCreate(BaseModel):
    nombre: str
    precio: int
    disponible: bool = True
    imagen_url: str
    kcal: int
    p: int
    f: int
    c: int

class Producto(BaseModel): 
    id: UUID4
    nombre: str
    macros: Macros
    disponible: bool
    precio: int
    imagen_url: str

    class Config:
        from_attributes = True

# --- 3. CARRITO ---

# Input para agregar
class ItemCarritoCreate(BaseModel):
    producto_id: str
    cantidad: int = 1

# Modelos base de Bowl
class Extra(BaseModel):
    nombre: str
    precio: int
    esLacteo: bool

class TipoBowl(BaseModel):
    nombre: str
    esVegano: bool
    maxProteinas: int

class BowlPersonalizado(BaseModel):
    tipo_bowl: TipoBowl
    extras: List[Extra]

# Item de respuesta (Con datos del producto incrustados)
class ItemCarrito(BaseModel):
    id: UUID4
    producto_id: Optional[UUID4]
    bowl_personalizado_id: Optional[UUID4]
    cantidad: int
    precio_unitario: int
    
    # IMPORTANTE: Esto permite ver el nombre y la foto en el JSON
    producto: Optional[Producto] = None
    bowl_personalizado: Optional[BowlPersonalizado] = None

    class Config:
        from_attributes = True

# Carrito completo de respuesta (Renombrado a CarritoView)
class CarritoView(BaseModel):
    id: UUID4
    usuario_id: UUID4
    items: List[ItemCarrito]
    total: int

    class Config:
        from_attributes = True

# --- 4. OTROS ---
class Filtro(BaseModel):
    tipos: Optional[List[str]] = None
    query: Optional[str] = None
    page: int = 1
    size: int = 8

class Promocion(BaseModel):
    id: UUID4
    nombre: str
    prioridad: PrioridadPromo
    descuento_porc: int

class Direccion(BaseModel):
    calle: str
    numero: str
    comuna: str
    depto: Optional[str] = None
    referencia: Optional[str] = None

class CotizacionEnvio(BaseModel):
    costo: int
    tiempo_estimado_min: int
    tiempo_estimado_max: int
    es_valido: bool

class Pedido(BaseModel):
    id: UUID4
    estado: EstadoPedido
    total: int
    
class ResultadoCancelacion(BaseModel):
    exito: bool
    mensaje: str
    pedido: Pedido

class DatosBoleta(BaseModel):
    rut: str
    email: EmailStr
    razon_social: str

class ResultadoBoleta(BaseModel):
    exito: bool
    folio: Optional[str]
    pdf_url: Optional[str]
    error: Optional[str]

class DatosFactura(BaseModel):
    rut: str
    email: EmailStr
    razon_social: str
    giro: str
    direccion_comercial: str
    comuna: str

class ResultadoFactura(BaseModel):
    exito: bool
    folio: Optional[str]
    pdf_url: Optional[str]
    error: Optional[str]

class AsignarRol(BaseModel):
    email_usuario: EmailStr
    rol: str

class AsignacionDespacho(BaseModel):
    metodo: str
    repartidor_id: Optional[str]

class ResultadoAsignacion(BaseModel):
    mensaje: str
    pedido_id: str
    eta_actualizada: str

class PedidoColaCocina(BaseModel):
    id: str
    promesa_entrega: str
    estado: str
    items: str