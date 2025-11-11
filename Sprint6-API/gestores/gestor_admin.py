# En: gestores/gestor_admin.py
from fastapi import APIRouter, Depends
from modelos import schemas
from typing import List

# Simulación de un "super admin"
async def get_admin_user():
    print("Verificando permisos de Administrador (simulación)")
    # Aquí iría la lógica de E01 para validar roles
    return {"username": "admin"}

router = APIRouter(
    prefix="/admin",
    tags=["Panel de Administración"],
    dependencies=[Depends(get_admin_user)] # Todas estas rutas requieren ser Admin
)

# --- Endpoint para E01: Asignar Roles ---
@router.post("/roles/asignar")
async def asignar_rol(asignacion: schemas.AsignarRol):
    """
    Lógica de E01:
    1. 'RoleService.assignRole()'.
    2. Registrar auditoría.
    """
    print(f"Asignando rol {asignacion.rol} a {asignacion.email_usuario}")
    return {"mensaje": "Rol asignado"}

# --- Endpoint para E04: Reporte de Ventas ---
@router.get("/reportes/ventas")
async def reporte_ventas(fecha_desde: str, fecha_hasta: str):
    """
    Lógica de E04:
    1. 'ReportService.salesSummary()'.
    2. Devolver KPIs y tabla.
    """
    print(f"Generando reporte de ventas de {fecha_desde} a {fecha_hasta}")
    return {
        "ingresos": 5420000,
        "pedidos": 684,
        "ticket_promedio": 7927,
        "tabla_datos": [
            {"fecha": "2025-09-24", "canal": "Web", "monto": 358000}
        ]
    }

# --- Endpoint para E03: Asignación de Despacho ---
@router.post("/despacho/{pedido_id}/asignar", response_model=schemas.ResultadoAsignacion)
async def asignar_despacho(
    pedido_id: str,
    asignacion: schemas.AsignacionDespacho
):
    """
    Lógica de E03:
    1. Si 'Auto-asignar', buscar repartidor disponible.
    2. Si 'Manual', asignar a 'repartidor_id'.
    """
    print(f"Asignando despacho para pedido {pedido_id}...")
    
    return schemas.ResultadoAsignacion(
        mensaje="Asignación realizada",
        pedido_id=pedido_id,
        eta_actualizada="32 min"
    )

# --- Endpoint para E05: Cola de Cocina (con WebSocket) ---
# (Nota: Los WebSockets son más avanzados, empezamos con un GET simple)
@router.get("/cocina/cola", response_model=List[schemas.PedidoColaCocina])
async def obtener_cola_cocina():
    """
    Lógica de E05 (versión simple):
    1. 'KitchenQueueService.listQueue()'.
    2. Devuelve la lista priorizada.
    (La versión avanzada usaría WebSockets para 'subscribeAWS()')
    """
    print("Obteniendo cola de cocina...")
    
    # Simulación de datos
    return [
        schemas.PedidoColaCocina(
            id="12345", promesa="12:10", ventana="12:05-12:15", llegada="11:58",
            estado="En cola", items="Ensalada, Sandwich"
        ),
        schemas.PedidoColaCocina(
            id="12346", promesa="12:12", ventana="12:10-12:20", llegada="12:01",
            estado="En cola", items="Wrap, Jugo"
        )
    ]