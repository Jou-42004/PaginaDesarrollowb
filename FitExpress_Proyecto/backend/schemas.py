from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- USUARIOS ---
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    rut: str
    telefono: str
    direccion: str
    comuna: str
    region: Optional[str] = "Metropolitana"

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    comuna: Optional[str] = None
    region: Optional[str] = None

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rut: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    comuna: Optional[str] = None
    region: Optional[str] = None
    rol: str = "cliente"
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioOut

# --- ADMIN ---
class CambioRol(BaseModel):
    nuevo_rol: str

# --- PRODUCTOS ---
class ProductoCreate(BaseModel):
    nombre: str
    precio_base: int
    imagen_url: str
    descripcion: str
    tipo: str
    kcal: int = 0
    proteina: float = 0
    grasas: float = 0
    carbs: float = 0
    disponible: bool = True

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio_base: Optional[int] = None
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None
    disponible: Optional[bool] = None

class ProductoOut(BaseModel):
    id: int
    nombre: str
    precio_base: int
    imagen_url: str
    tipo: str
    macros: Optional[dict] = None
    disponible: bool
    class Config: from_attributes = True

# --- CARRITO (AQUÍ ESTABA EL ERROR) ---
class CarritoItemCreate(BaseModel):
    producto_id: int
    cantidad: int
    personalizacion: Optional[str] = None
    precio_custom: Optional[int] = None # <--- ESTO FALTABA PARA GUARDAR EL PRECIO

class CarritoItemOut(BaseModel):
    id: int
    producto: ProductoOut
    cantidad: int
    precio_unitario: int
    personalizacion: Optional[str] = None

class CarritoOut(BaseModel):
    items: List[CarritoItemOut]
    total: int

# --- PEDIDOS ---
class PedidoCreate(BaseModel):
    direccion_envio: str
    metodo_pago: str
    tipo_entrega: str

class ItemPedidoOut(BaseModel):
    nombre_producto: str
    cantidad: int
    precio_unitario: int
    total: int 
    personalizacion: Optional[str] = None

class PedidoOut(BaseModel):
    id: int
    total: int
    estado: str
    fecha_creacion: datetime
    direccion_envio: Optional[str] = "Retiro"
    items: List[ItemPedidoOut]
    usuario: UsuarioOut
    class Config: from_attributes = True

# --- FACTURACIÓN ---
class EmailRequest(BaseModel):
    email: str
    tipo_documento: str