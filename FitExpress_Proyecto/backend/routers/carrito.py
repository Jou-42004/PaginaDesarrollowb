from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/carrito", tags=["Carrito"])

@router.get("/", response_model=schemas.CarritoOut)
def get_cart(user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    
    # Crear carrito si no existe (lazy creation)
    if not carrito:
        carrito = models.Carrito(usuario_id=user.id)
        db.add(carrito)
        db.commit()
        return {"items": [], "total": 0}
    
    formatted_items = []
    total_amount = 0
    
    for item in carrito.items:
        prod = item.producto
        
        # Determinar precio: usar el personalizado si existe, sino el base
        precio_unitario = item.precio_guardado if item.precio_guardado is not None else prod.precio_base
        
        # Estructurar datos del producto para el schema de respuesta
        prod_data = {
            "id": prod.id,
            "nombre": prod.nombre,
            "precio_base": prod.precio_base,
            "imagen_url": prod.imagen_url,
            "tipo": prod.tipo,
            "disponible": prod.disponible,
            "macros": {
                "kcal": prod.kcal, 
                "p": prod.proteina, 
                "f": prod.grasas, 
                "c": prod.carbs
            }
        }

        formatted_items.append({
            "id": item.id,
            "producto": prod_data, 
            "cantidad": item.cantidad,
            "precio_unitario": precio_unitario, 
            "personalizacion": item.personalizacion
        })
        
        total_amount += precio_unitario * item.cantidad
        
    return {"items": formatted_items, "total": total_amount}

@router.post("/items")
def add_item_to_cart(item_in: schemas.CarritoItemCreate, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    
    if not carrito:
        carrito = models.Carrito(usuario_id=user.id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)

    # Lógica de agrupación:
    # Si el producto tiene personalización o precio custom, se trata como ítem único (nueva fila).
    # Si es un producto estándar, se busca si ya existe para sumar cantidad.
    
    is_custom_item = item_in.personalizacion or item_in.precio_custom

    if is_custom_item:
        new_item = models.CarritoItem(
            carrito_id=carrito.id, 
            producto_id=item_in.producto_id,
            cantidad=item_in.cantidad, 
            personalizacion=item_in.personalizacion,
            precio_guardado=item_in.precio_custom
        )
        db.add(new_item)
    else:
        existing_item = db.query(models.CarritoItem).filter(
            models.CarritoItem.carrito_id == carrito.id,
            models.CarritoItem.producto_id == item_in.producto_id,
            models.CarritoItem.personalizacion == None
        ).first()

        if existing_item:
            existing_item.cantidad += item_in.cantidad
        else:
            new_item = models.CarritoItem(
                carrito_id=carrito.id, 
                producto_id=item_in.producto_id, 
                cantidad=item_in.cantidad
            )
            db.add(new_item)
    
    db.commit()
    return {"mensaje": "Producto agregado al carrito"}

@router.delete("/items/{item_id}")
def remove_item(item_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    item = db.query(models.CarritoItem).join(models.Carrito).filter(
        models.CarritoItem.id == item_id, 
        models.Carrito.usuario_id == user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    db.delete(item)
    db.commit()
    return {"mensaje": "Item eliminado"}

@router.delete("/")
def clear_cart(user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    if carrito:
        db.query(models.CarritoItem).filter(models.CarritoItem.carrito_id == carrito.id).delete()
        db.commit()
    return {"mensaje": "Carrito vaciado"}