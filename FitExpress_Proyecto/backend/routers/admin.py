from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/admin", tags=["Panel Admin"])

# --- SEGURIDAD ---
def solo_admin(user: models.Usuario = Depends(get_user_from_token)):
    if user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")
    return user

# --- FUNCIÓN AUXILIAR (¡LA CLAVE!) ---
def formatear_pedido(p):
    # Convertimos los items a diccionario manualmente para asegurar que lleguen al frontend
    items_list = []
    for i in p.items:
        items_list.append({
            "nombre_producto": i.nombre_producto,
            "cantidad": i.cantidad,
            "precio_unitario": i.precio_unitario,
            "total": i.precio_unitario * i.cantidad,
            "personalizacion": i.personalizacion
        })
    
    # Devolvemos la estructura que espera el frontend
    return {
        "id": p.id,
        "total": p.total,
        "estado": p.estado,
        "fecha_creacion": p.fecha_creacion,
        "direccion_envio": p.direccion_envio,
        "repartidor": p.repartidor,
        "items": items_list, # ¡Aquí van los productos!
        "usuario": p.usuario
    }

# --- 1. COCINA (COLA DE PREPARACIÓN) ---
@router.get("/pedidos/activos")
def ver_cola_cocina(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    pedidos = db.query(models.Pedido).filter(
        models.Pedido.estado.in_(["Recibido", "En preparacion", "Pagado"])
    ).order_by(models.Pedido.fecha_creacion.asc()).all()
    
    # Usamos la función de formateo
    return [formatear_pedido(p) for p in pedidos]

@router.put("/pedidos/{id}/estado")
def cambiar_estado_pedido(id: int, estado: str, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    p = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if not p: raise HTTPException(404, "Pedido no encontrado")
    p.estado = estado
    db.commit()
    return {"mensaje": "Estado actualizado"}

# --- 2. GESTIÓN DE USUARIOS ---
@router.get("/usuarios", response_model=List[schemas.UsuarioOut])
def listar_usuarios(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    return db.query(models.Usuario).all()

@router.put("/usuarios/{user_id}/rol")
def cambiar_rol(user_id: int, datos: schemas.CambioRol, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    if user_id == admin.id and datos.nuevo_rol != "admin": raise HTTPException(400, "Error de seguridad")
    u = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    u.rol = datos.nuevo_rol
    db.commit()
    return {"mensaje": "Rol actualizado"}

@router.get("/usuarios/{user_id}/historial")
def historial_usuario(user_id: int, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    pedidos = db.query(models.Pedido).filter(models.Pedido.usuario_id == user_id).order_by(models.Pedido.fecha_creacion.desc()).all()
    return [formatear_pedido(p) for p in pedidos]

# --- 3. GESTIÓN PRODUCTOS ---
@router.get("/productos", response_model=List[schemas.ProductoOut])
def listar_productos(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    return db.query(models.Producto).order_by(models.Producto.id).all()

@router.post("/productos", response_model=schemas.ProductoOut)
def crear_producto(prod: schemas.ProductoCreate, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    nuevo = models.Producto(**prod.dict())
    db.add(nuevo); db.commit(); db.refresh(nuevo)
    return nuevo

@router.put("/productos/{pid}")
def editar_producto(pid: int, datos: schemas.ProductoUpdate, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    p = db.query(models.Producto).filter(models.Producto.id == pid).first()
    for key, value in datos.dict(exclude_unset=True).items(): setattr(p, key, value)
    db.commit(); db.refresh(p)
    return p

@router.delete("/productos/{pid}")
def eliminar_producto(pid: int, db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    db.query(models.Producto).filter(models.Producto.id == pid).delete()
    db.commit()
    return {"mensaje": "Eliminado"}

# --- 4. REPORTES ---
@router.get("/reportes/ventas")
def reporte_ventas(db: Session = Depends(database.get_db), admin=Depends(solo_admin)):
    pedidos = db.query(models.Pedido).filter(models.Pedido.estado != "Cancelado").all()
    total = sum(p.total for p in pedidos)
    count = len(pedidos)
    return {"total_ventas": total, "cantidad_pedidos": count, "ticket_promedio": int(total/count) if count>0 else 0}