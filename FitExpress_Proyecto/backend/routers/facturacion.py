from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/facturacion", tags=["Facturación"])

@router.get("/datos/{pedido_id}")
def datos_factura(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id, models.Pedido.usuario_id == user.id).first()
    if not pedido: raise HTTPException(status_code=404)
    
    return {
        "usuario": {
            "nombre": user.nombre, "email": user.email, "rut": user.rut, "direccion": user.direccion
        },
        "pedido": {
            "id": pedido.id, "total": pedido.total, "fecha": pedido.fecha_creacion,
            "items": [{"nombre": i.nombre_producto, "precio": i.precio_unitario} for i in pedido.items]
        },
        "empresa": {
            "nombre": "Fit Express SpA", "rut": "76.543.210-1", "direccion": "Av. Principal 1234"
        }
    }