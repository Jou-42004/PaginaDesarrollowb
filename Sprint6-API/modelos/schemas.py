# En: modelos/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from enum import Enum

# --- Enums (Basado en tus diagramas) ---
class EstadoUsuario(str, Enum):
    ACTIVO = "Activo"
    PENDIENTE = "Pendiente"

class PrioridadPromo(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

class EstadoPedido(str, Enum):
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    FALLIDO = "Fallido"
    EN_PREPARACION = "En preparación"
    EN_RUTA = "En ruta"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

# --- B01/B02/B03: Modelos de Usuario ---

class Usuario(BaseModel):
    id: str # uuid
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
    direccion: str # Del B01, luego se usa en B11
    comuna: str
    region: str
    telefono: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class CambioPassword(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str
    confirmar_nueva: str

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario # Devolvemos los datos del usuario al loguear

# --- B05/B06: Modelos de Producto y Filtro ---

class Macros(BaseModel):
    kcal: int
    p: int # Proteínas
    f: int # Grasas (Fat)
    c: int # Carbos

class Producto(BaseModel):
    id: str # uuid
    nombre: str
    macros: Macros
    disponible: bool
    precio_base: float
    imagen_url: str

class Filtro(BaseModel):
    tipos: Optional[List[str]] = None # Vegano, Proteico, Sin gluten
    query: Optional[str] = None
    page: int = 1
    size: int = 8

# --- B08: Modelos de Promociones ---

class Promocion(BaseModel):
    id: str # uuid
    nombre: str
    prioridad: PrioridadPromo
    descuento_porc: int

# --- B10/B09: Modelos de Pedido y Carrito ---

class Extra(BaseModel):
    nombre: str
    precio: int
    esLacteo: bool

class TipoBowl(BaseModel):
    nombre: str
    esVegano: bool
    permiteLacteos: bool
    maxProteinas: int

class BowlPersonalizado(BaseModel):
    tipo_bowl: TipoBowl
    extras: List[Extra]
    salsas: List[str]

class ItemCarrito(BaseModel):
    producto_id: Optional[str] = None # ID del producto (si es B05)
    bowl_personalizado: Optional[BowlPersonalizado] = None # Si es (B10)
    cantidad: int
    precio_unitario: int

class Carrito(BaseModel):
    id: str # uuid
    usuario_id: str
    items: List[ItemCarrito]
    subtotal: int
    descuentos: int
    total: int

# --- B11: Modelos de Dirección y Envío ---

class Direccion(BaseModel):
    calle: str
    numero: str
    depto: Optional[str] = None
    comuna: str
    referencia: Optional[str] = None

class CotizacionEnvio(BaseModel):
    costo: int
    tiempo_estimado_min: int
    tiempo_estimado_max: int
    es_valido: bool # Cobertura

# --- B12: Modelos de Cancelación ---

class Pedido(BaseModel):
    id: str
    estado: EstadoPedido
    total: int
    metodo_pago: str
    
class ResultadoCancelacion(BaseModel):
    exito: bool
    mensaje: str
    pedido: Pedido # El pedido actualizado

# --- B15/B16: Modelos de Facturación (Billing) ---

class DatosFacturacionBase(BaseModel):
    rut: str
    email: EmailStr

class DatosBoleta(DatosFacturacionBase):
    razon_social: str # Nombre

class ResultadoBoleta(BaseModel):
    exito: bool
    folio: Optional[str] = None
    pdf_url: Optional[str] = None
    error: Optional[str] = None

class DatosFactura(DatosFacturacionBase):
    razon_social: str
    giro: str
    direccion_comercial: str
    comuna: str

class ResultadoFactura(BaseModel):
    exito: bool
    folio: Optional[str] = None
    pdf_url: Optional[str] = None
    error: Optional[str] = None

# --- E01/E03/E04/E05: Modelos de Admin ---

class AsignarRol(BaseModel):
    email_usuario: EmailStr
    rol: str

class AsignacionDespacho(BaseModel):
    metodo: str # "Auto-asignar" o "Manual"
    repartidor_id: Optional[str] = None

class ResultadoAsignacion(BaseModel):
    mensaje: str
    pedido_id: str
    eta_actualizada: str

class PedidoColaCocina(BaseModel):
    id: str
    promesa_entrega: str # "12:10"
    ventana: str # "12:05-12:15"
    llegada: str # "11:58"
    estado: str # "En cola", "En preparación"
    items: str # "Ensalada, Sandwich"