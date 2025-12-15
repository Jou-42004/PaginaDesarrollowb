from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/admin", tags=["Panel Admin"])

# Dependencia de seguridad
def solo_admin(user: models.Usuario = Depends(get_user_from_token)):
    if user.rol != "admin":
        raise HTTPException(status_code=403, detail="Requiere privilegios de administrador.")
    return user

# Helper para serializar pedidos manualmente y evitar problemas con Pydantic
def _formatear_pedido(pedido):
    items_list = [
        {
            "nombre_producto": item.nombre_producto,
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario,
            "total": item.precio_unitario * item.cantidad,
            "personalizacion": item.personalizacion
        }
        for item in pedido.items
    ]
    
    return {
        "id": pedido.id,
        "total": pedido.total,
        "estado": pedido.estado,
        "fecha_creacion": pedido.fecha_creacion,
        "direccion_envio": pedido.direccion_envio,
        "metodo_pago": pedido.metodo_pago,
        "repartidor": pedido.repartidor,
        "items": items_list, 
        "usuario": {
            "id": pedido.usuario.id,
            "nombre": pedido.usuario.nombre,
            "email": pedido.usuario.email
        }
    }

# ----------------------
# COCINA Y PEDIDOS
# ----------------------

@router.get("/pedidos/activos")
def get_cola_cocina(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    estados_activos = ["Recibido", "En preparacion", "Pagado"]
    pedidos = db.query(models.Pedido).filter(
        models.Pedido.estado.in_(estados_activos)
    ).order_by(models.Pedido.fecha_creacion.asc()).all()
    
    return [_formatear_pedido(p) for p in pedidos]

@router.put("/pedidos/{id}/estado")
def update_estado_pedido(id: int, estado: str, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    pedido.estado = estado
    db.commit()
    return {"mensaje": "Estado actualizado correctamente"}

# ----------------------
# GESTIÓN DE USUARIOS
# ----------------------

@router.get("/usuarios", response_model=List[schemas.UsuarioOut])
def get_usuarios(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    return db.query(models.Usuario).all()

@router.put("/usuarios/{user_id}/rol")
def update_rol_usuario(user_id: int, datos: schemas.CambioRol, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    if user_id == admin.id and datos.nuevo_rol != "admin":
        raise HTTPException(status_code=400, detail="No puedes revocar tu propio permiso de administrador.")
    
    usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.rol = datos.nuevo_rol
    db.commit()
    return {"mensaje": "Rol actualizado"}

@router.get("/usuarios/{user_id}/historial")
def get_historial_usuario(user_id: int, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    pedidos = db.query(models.Pedido).filter(
        models.Pedido.usuario_id == user_id
    ).order_by(models.Pedido.fecha_creacion.desc()).all()
    
    return [_formatear_pedido(p) for p in pedidos]

# ----------------------
# GESTIÓN DE PRODUCTOS
# ----------------------

@router.get("/productos", response_model=List[schemas.ProductoOut])
def get_productos(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    return db.query(models.Producto).order_by(models.Producto.id).all()

@router.post("/productos", response_model=schemas.ProductoOut)
def create_producto(prod: schemas.ProductoCreate, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    nuevo_producto = models.Producto(**prod.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@router.put("/productos/{pid}")
def update_producto(pid: int, datos: schemas.ProductoUpdate, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    producto = db.query(models.Producto).filter(models.Producto.id == pid).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Actualizar solo los campos que vienen en la petición
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    
    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/productos/{pid}")
def delete_producto(pid: int, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    producto = db.query(models.Producto).filter(models.Producto.id == pid).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado"}

# ----------------------
# REPORTES
# ----------------------

@router.get("/reportes/ventas")
def get_reporte_ventas(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    pedidos_validos = db.query(models.Pedido).filter(models.Pedido.estado != "Cancelado").all()
    
    total_ventas = sum(p.total for p in pedidos_validos)
    cantidad = len(pedidos_validos)
    ticket_promedio = int(total_ventas / cantidad) if cantidad > 0 else 0
    
    return {
        "total_ventas": total_ventas,
        "cantidad_pedidos": cantidad,
        "ticket_promedio": ticket_promedio
    }