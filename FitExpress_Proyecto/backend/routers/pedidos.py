from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# --- FUNCIÓN AUXILIAR PARA FORMATEAR ---
# Esta función convierte los objetos de la BD en diccionarios simples
# para evitar errores de Pydantic.
def format_pedido_response(pedido, user):
    # 1. Formatear Items
    items_fmt = []
    for i in pedido.items:
        items_fmt.append({
            "nombre_producto": i.nombre_producto,
            "cantidad": i.cantidad,
            "precio_unitario": i.precio_unitario,
            "total": i.precio_unitario * i.cantidad,
            "personalizacion": i.personalizacion
        })

    # 2. Formatear Usuario (Convertir a dict simple)
    user_dict = {
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "rut": user.rut,
        "direccion": user.direccion,
        "telefono": user.telefono,
        "comuna": user.comuna,
        "region": user.region,
        "rol": user.rol
    }

    # 3. Retornar estructura limpia
    return {
        "id": pedido.id,
        "total": pedido.total,
        "estado": pedido.estado,
        "fecha_creacion": pedido.fecha_creacion,
        "direccion_envio": pedido.direccion_envio,
        "usuario": user_dict, 
        "items": items_fmt
    }

# --- ENDPOINTS ---

@router.post("/crear")
def crear(datos: schemas.PedidoCreate, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    if not carrito or not carrito.items:
        raise HTTPException(status_code=400, detail="El carrito está vacío")
    
    # Calcular total
    subtotal = sum([i.producto.precio_base * i.cantidad for i in carrito.items])
    
    # Calcular Envío (Si es delivery, sumamos 2000)
    costo_envio = 2000 if datos.tipo_entrega == "delivery" else 0
    total_final = subtotal + costo_envio
    
    pedido = models.Pedido(
        usuario_id=user.id,
        total=total_final,
        direccion_envio=datos.direccion_envio,
        metodo_pago=datos.metodo_pago,
        estado="Recibido"
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    
    for item in carrito.items:
        db.add(models.ItemPedido(
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            nombre_producto=item.producto.nombre,
            precio_unitario=item.producto.precio_base,
            cantidad=item.cantidad,
            personalizacion=item.personalizacion
        ))
    
    db.query(models.CarritoItem).filter(models.CarritoItem.carrito_id == carrito.id).delete()
    db.commit()
    
    return {"mensaje": "Pedido creado", "pedido_id": pedido.id}

@router.get("/{pedido_id}", response_model=schemas.PedidoOut)
def ver(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id, models.Pedido.usuario_id == user.id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Usamos la función segura
    return format_pedido_response(pedido, user)

@router.get("/mis_pedidos", response_model=List[schemas.PedidoOut])
def historial(user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    pedidos = db.query(models.Pedido).filter(models.Pedido.usuario_id == user.id).order_by(models.Pedido.fecha_creacion.desc()).all()
    
    # Convertimos CADA pedido usando la función segura
    return [format_pedido_response(p, user) for p in pedidos]

@router.put("/{pedido_id}/cancelar")
def cancelar(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    p = db.query(models.Pedido).filter(models.Pedido.id == pedido_id, models.Pedido.usuario_id == user.id).first()
    if not p: raise HTTPException(404)
    
    if p.estado not in ["Recibido", "Aprobado", "Pendiente", "Pagado"]:
        raise HTTPException(status_code=400, detail="No se puede cancelar")
        
    p.estado = "Cancelado"
    db.commit()
    return {"mensaje": "Cancelado"}

@router.put("/{pedido_id}/pagar")
def pagar(pedido_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    p = db.query(models.Pedido).filter(models.Pedido.id == pedido_id, models.Pedido.usuario_id == user.id).first()
    if not p: raise HTTPException(404)
    p.estado = "Pagado"
    db.commit()
    return {"mensaje": "Pagado"}