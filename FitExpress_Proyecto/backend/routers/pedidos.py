from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# Helper para formatear respuesta y evitar problemas de validación con Pydantic
def _formatear_pedido_response(pedido, usuario):
    items_fmt = [
        {
            "nombre_producto": item.nombre_producto,
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario,
            "total": item.precio_unitario * item.cantidad,
            "personalizacion": item.personalizacion
        }
        for item in pedido.items
    ]

    # Convertir usuario a dict para evitar conflictos con el ORM
    usuario_dict = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rut": usuario.rut,
        "direccion": usuario.direccion,
        "telefono": usuario.telefono,
        "comuna": usuario.comuna,
        "region": usuario.region,
        "rol": usuario.rol
    }
    
    return {
        "id": pedido.id,
        "total": pedido.total,
        "estado": pedido.estado,
        "fecha_creacion": pedido.fecha_creacion,
        "direccion_envio": pedido.direccion_envio,
        "usuario": usuario_dict,
        "items": items_fmt
    }
    
@router.post("/crear")
def crear_pedido(datos: schemas.PedidoCreate, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    
    if not carrito or not carrito.items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")
    
    # Calcular totales
    subtotal = 0
    for item in carrito.items:
        # Usar precio personalizado si existe, sino el base del producto
        precio_real = item.precio_guardado if item.precio_guardado is not None else item.producto.precio_base
        subtotal += precio_real * item.cantidad

    costo_envio = 2000 if datos.tipo_entrega == "delivery" else 0
    total_final = subtotal + costo_envio
    
    # Crear pedido
    nuevo_pedido = models.Pedido(
        usuario_id=user.id,
        total=total_final,
        direccion_envio=datos.direccion_envio,
        metodo_pago=datos.metodo_pago,
        estado="Recibido"
    )
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    # Mover items del carrito al pedido (Snapshot de precios)
    for item in carrito.items:
        precio_real = item.precio_guardado if item.precio_guardado is not None else item.producto.precio_base
        
        # Si tiene personalización, usamos ese texto como nombre o detalle
        nombre_final = item.personalizacion if item.personalizacion else item.producto.nombre

        db.add(models.ItemPedido(
            pedido_id=nuevo_pedido.id,
            producto_id=item.producto_id,
            nombre_producto=nombre_final, 
            precio_unitario=precio_real,
            cantidad=item.cantidad,
            personalizacion=item.personalizacion
        ))
    
    # Vaciar carrito
    db.query(models.CarritoItem).filter(models.CarritoItem.carrito_id == carrito.id).delete()
    db.commit()
    
    return {"mensaje": "Pedido creado exitosamente", "pedido_id": nuevo_pedido.id}

@router.get("/{pedido_id}", response_model=schemas.PedidoOut)
def ver_pedido(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id, 
        models.Pedido.usuario_id == user.id
    ).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return _formatear_pedido_response(pedido, user)

@router.get("/mis_pedidos", response_model=List[schemas.PedidoOut])
def listar_historial(user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedidos = db.query(models.Pedido).filter(
        models.Pedido.usuario_id == user.id
    ).order_by(models.Pedido.fecha_creacion.desc()).all()
    
    return [_formatear_pedido_response(p, user) for p in pedidos]

@router.put("/{pedido_id}/cancelar")
def cancelar_pedido(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id, 
        models.Pedido.usuario_id == user.id
    ).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    estados_cancelables = ["Recibido", "Aprobado", "Pendiente", "Pagado"]
    if pedido.estado not in estados_cancelables:
        raise HTTPException(status_code=400, detail="No es posible cancelar el pedido en su estado actual")
        
    pedido.estado = "Cancelado"
    db.commit()
    return {"mensaje": "Pedido cancelado correctamente"}

@router.put("/{pedido_id}/pagar")
def pagar_pedido(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id, 
        models.Pedido.usuario_id == user.id
    ).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    pedido.estado = "Pagado"
    db.commit()
    return {"mensaje": "Pago registrado exitosamente"}