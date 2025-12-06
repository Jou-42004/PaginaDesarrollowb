from fastapi import APIRouter, Depends
from modelos import schemas
from .gestor_usuarios import get_usuario_actual

router = APIRouter(
    prefix="/pedidos",
    tags=["Gestión de Pedidos y Pago"],
    dependencies=[Depends(get_usuario_actual)]
)

# --- Endpoint para B11: Cotizar Envío ---
@router.post("/cotizar-envio", response_model=schemas.CotizacionEnvio)
async def cotizar_envio(
    direccion: schemas.Direccion, # Usa el schema de entrada
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    print(f"Cotizando envío para comuna: {direccion.comuna}")
    
    comunas_validas = ["Providencia", "Santiago", "Las Condes", "Ñuñoa", "La Reina"]
    
    if direccion.comuna in comunas_validas:
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
            es_valido=False
        )

# --- Endpoint para Cancelar (B12) ---
@router.post("/{pedido_id}/cancelar", response_model=schemas.ResultadoCancelacion)
async def cancelar_pedido(
    pedido_id: str,
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    # Simulación de pedido
    pedido_mock = schemas.Pedido(
        id=pedido_id,
        estado=schemas.EstadoPedido.CANCELADO,
        total=10000,
        metodo_pago="Tarjeta"
    )
    
    return schemas.ResultadoCancelacion(
        exito=True,
        mensaje="Pedido cancelado exitosamente",
        pedido=pedido_mock
    )