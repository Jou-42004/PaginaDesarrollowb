# En: gestores/gestor_pedidos.py
from fastapi import APIRouter, Depends
from modelos import schemas
from typing import Any

# Importamos el "login" del gestor de usuarios
from .gestor_usuarios import get_usuario_actual

router = APIRouter(
    prefix="/pedidos",
    tags=["Gestión de Pedidos y Pago"],
    dependencies=[Depends(get_usuario_actual)] # ¡Todas estas rutas están protegidas!
)

# --- Endpoint para B10: Crear Pedido (Checkout) ---
@router.post("/", response_model=schemas.Pedido)
async def crear_pedido(
    carrito: schemas.Carrito,
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    """
    Recibe el Carrito (B09) con los items (B10).
    Aquí va la lógica:
    1. Validar stock (Inventario).
    2. Aplicar promociones (B08) y recalcular total (B09).
    3. Crear el Pedido en la BD con estado "Pendiente".
    4. Iniciar el pago (E02).
    """
    print(f"Usuario {usuario.email} está creando un pedido.")
    
    # ... Lógica de creación de pedido ...
    
    # Simulación de respuesta
    pedido_creado = schemas.Pedido(
        id="pedido-uuid-12345",
        estado=schemas.EstadoPedido.PENDIENTE,
        total=carrito.total,
        metodo_pago="Por definir"
    )
    return pedido_creado

# --- Endpoint para B11: Cotizar Envío ---
@router.post("/cotizar-envio", response_model=schemas.CotizacionEnvio)
async def cotizar_envio(
    direccion: schemas.Direccion,
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    """
    Recibe la dirección de B11 y valida cobertura.
    """
    print(f"Cotizando envío para comuna: {direccion.comuna}")
    
    # ... Lógica de validación de cobertura y cálculo ...
    
    if direccion.comuna == "Providencia":
        return schemas.CotizacionEnvio(
            costo=2000,
            tiempo_estimado_min=35,
            tiempo_estimado_max=45,
            es_valido=True
        )
    else:
        return schemas.CotizacionEnvio(
            costo=0,
            tiempo_estimado_min=0,
            tiempo_estimado_max=0,
            es_valido=False # Fuera de cobertura
        )

# --- Endpoint para B12: Cancelar Pedido ---
@router.post("/{pedido_id}/cancelar", response_model=schemas.ResultadoCancelacion)
async def cancelar_pedido(
    pedido_id: str,
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    """
    Lógica de B12:
    1. Buscar pedido en BD.
    2. Verificar que pertenece al usuario.
    3. Validar 'puedeCancelar()' (Estado "Recibido" o "Aprobado").
    4. Cambiar estado a "Cancelado".
    5. Procesar reembolso (ServicioCancelacion).
    6. Enviar email (NotificadorCorreo).
    """
    print(f"Usuario {usuario.email} intenta cancelar pedido {pedido_id}")
    
    # ... Lógica de cancelación ...
    
    # Simulación de éxito
    pedido_simulado = schemas.Pedido(
        id=pedido_id,
        estado=schemas.EstadoPedido.CANCELADO, # Nuevo estado
        total=10775,
        metodo_pago="Tarjeta"
    )
    return schemas.ResultadoCancelacion(
        exito=True,
        mensaje="Pedido cancelado exitosamente.",
        pedido=pedido_simulado
    )

# --- Endpoint para E02/B20: Webhook de Pagos ---
# Este endpoint NO debe estar protegido, ya que lo llama un servicio externo.
@router.post("/pago/webhook", include_in_schema=False)
async def webhook_pago(payload: Any):
    """
    Ruta que escucha al proveedor de pago (E02).
    1. Recibe el 'payload' (datos) del proveedor.
    2. Valida la firma del webhook.
    3. Si el pago fue exitoso:
        - Llama a 'marcarPagado()' en el Pedido (B20).
        - Genera la boleta/factura (B15/B16).
        - Envía el pedido a la cola de cocina (E05).
    """
    print("¡Webhook de pago recibido!")
    # ... Lógica de procesamiento de webhook ...
    return {"status": "recibido"}