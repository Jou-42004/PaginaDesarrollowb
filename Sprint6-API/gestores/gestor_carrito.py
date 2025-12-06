from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from modelos import schemas, models 
from .gestor_usuarios import get_usuario_actual
from database import get_session 

router = APIRouter(
    prefix="/carrito",
    tags=["Gestión del Carrito"],
    dependencies=[Depends(get_usuario_actual)]
)

# --- 1. Obtener el Carrito ---
@router.get("/", response_model=schemas.CarritoView)
async def obtener_carrito(
    usuario: schemas.Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_session)
):
    statement = select(models.Carrito).where(models.Carrito.usuario_id == usuario.id)
    carrito = db.exec(statement).first()

    if not carrito:
        carrito = models.Carrito(usuario_id=usuario.id, total=0)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    
    return carrito

# --- 2. Agregar Item al Carrito ---
@router.post("/items", response_model=schemas.CarritoView)
async def agregar_item(
    item_in: schemas.ItemCarritoCreate, 
    usuario: schemas.Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_session)
):
    # A. Obtener carrito
    statement = select(models.Carrito).where(models.Carrito.usuario_id == usuario.id)
    carrito = db.exec(statement).first()
    if not carrito:
        carrito = models.Carrito(usuario_id=usuario.id, total=0)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)

    # B. Buscar producto
    try:
        prod_id = UUID(item_in.producto_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    producto = db.get(models.Producto, prod_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if not producto.disponible:
        raise HTTPException(status_code=400, detail="El producto no está disponible")

    # C. Verificar si existe (Sumar cantidad)
    item_existente = next((item for item in carrito.items if item.producto_id == producto.id), None)

    if item_existente:
        item_existente.cantidad += item_in.cantidad
        db.add(item_existente)
    else:
        nuevo_item = models.ItemCarrito(
            carrito_id=carrito.id,
            producto_id=producto.id,
            cantidad=item_in.cantidad,
            precio_unitario=producto.precio 
        )
        db.add(nuevo_item)
    
    db.commit()
    db.refresh(carrito)

    # D. Recalcular total
    nuevo_total = sum([item.precio_unitario * item.cantidad for item in carrito.items])
    carrito.total = nuevo_total
    
    db.add(carrito)
    db.commit()
    db.refresh(carrito)
    
    return carrito

# --- 3. Eliminar Item ---
@router.delete("/items/{item_id}", response_model=schemas.CarritoView)
async def eliminar_item(
    item_id: str,
    usuario: schemas.Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_session)
):
    try:
        uuid_item = UUID(item_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")

    item = db.get(models.ItemCarrito, uuid_item)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    carrito = item.carrito
    if carrito.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No tienes permiso")

    db.delete(item)
    db.commit()
    
    db.refresh(carrito)
    carrito.total = sum([i.precio_unitario * i.cantidad for i in carrito.items])
    db.add(carrito)
    db.commit()
    db.refresh(carrito)

    return carrito

# --- 4. Vaciar Carrito ---
@router.delete("/", status_code=204)
async def vaciar_carrito(
    usuario: schemas.Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_session)
):
    statement = select(models.Carrito).where(models.Carrito.usuario_id == usuario.id)
    carrito = db.exec(statement).first()
    
    if carrito:
        for item in carrito.items:
            db.delete(item)
        
        carrito.total = 0
        db.add(carrito)
        db.commit()
    
    return None