# En: gestores/gestor_facturacion.py
from fastapi import APIRouter, Depends
from modelos import schemas
from .gestor_usuarios import get_usuario_actual

router = APIRouter(
    prefix="/facturacion",
    tags=["Facturación y Documentos"],
    dependencies=[Depends(get_usuario_actual)] # Protegido
)

# --- Endpoint para B15: Emitir Boleta ---
@router.post("/boleta", response_model=schemas.ResultadoBoleta)
async def emitir_boleta(
    datos: schemas.DatosBoleta,
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    """
    Lógica de B15:
    1. Validar RUT y email.
    2. Llamar al 'BillingService' para conectar con el SII.
    3. Si falla ("Servicio no disponible"), devolver error.
    """
    print(f"Emitiendo boleta para RUT: {datos.rut}")
    
    # ... Lógica de emisión ...
    
    # Simulación de éxito
    return schemas.ResultadoBoleta(
        exito=True,
        folio="123456",
        pdf_url="/boletas/123456.pdf"
    )

# --- Endpoint para B16: Emitir Factura ---
@router.post("/factura", response_model=schemas.ResultadoFactura)
async def emitir_factura(
    datos: schemas.DatosFactura,
    usuario: schemas.Usuario = Depends(get_usuario_actual)
):
    """
    Lógica de B16:
    1. Validar RUT, razón social, giro, etc.
    2. Llamar al 'BillingService'.
    """
    print(f"Emitiendo factura para RUT: {datos.rut}")
    
    # ... Lógica de emisión ...
    
    # Simulación de éxito
    return schemas.ResultadoFactura(
        exito=True,
        folio="F7890",
        pdf_url="/facturas/F7890.pdf"
    )