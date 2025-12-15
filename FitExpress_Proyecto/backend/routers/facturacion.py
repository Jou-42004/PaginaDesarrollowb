from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/facturacion", tags=["Facturación"])

@router.get("/datos/{pedido_id}")
def get_datos_factura(
    pedido_id: int, 
    user: models.Usuario = Depends(get_user_from_token), 
    db: Session = Depends(database.get_db)
):
    # Buscar el pedido verificando que pertenezca al usuario actual
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id, 
        models.Pedido.usuario_id == user.id
    ).first()
    
    if not pedido: 
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Formatear lista de productos para el documento
    items_detalle = [
        {
            "nombre": item.nombre_producto,
            "precio": item.precio_unitario,
            "cantidad": item.cantidad,
            "total_linea": item.precio_unitario * item.cantidad
        } 
        for item in pedido.items
    ]
    
    # Retornar estructura de datos para la boleta/factura
    return {
        "usuario": {
            "nombre": user.nombre,
            "email": user.email,
            "rut": user.rut,
            "direccion": user.direccion or "Sin dirección registrada"
        },
        "pedido": {
            "id": pedido.id,
            "total": pedido.total,
            "fecha": pedido.fecha_creacion,
            "items": items_detalle
        },
        "empresa": {
            "nombre": "Fit Express SpA",
            "rut": "76.543.210-1",
            "direccion": "Av. Principal 1234, Santiago"
        }
    }