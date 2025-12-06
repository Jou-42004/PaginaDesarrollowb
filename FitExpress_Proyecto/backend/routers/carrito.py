from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/carrito", tags=["Carrito"])

@router.get("/", response_model=schemas.CarritoOut)
def ver_carrito(user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    
    if not carrito:
        return {"items": [], "total": 0}
    
    items_res = []
    total = 0
    
    for item in carrito.items:
        prod = item.producto
        # USAR PRECIO GUARDADO SI EXISTE (Esto arregla el precio)
        precio_final = item.precio_guardado if item.precio_guardado is not None else prod.precio_base
        
        prod_dict = {
            "id": prod.id,
            "nombre": prod.nombre,
            "precio_base": prod.precio_base,
            "imagen_url": prod.imagen_url,
            "tipo": prod.tipo,
            "disponible": prod.disponible,
            "macros": {"kcal": prod.kcal, "p": prod.proteina, "f": prod.grasas, "c": prod.carbs}
        }

        items_res.append({
            "id": item.id,
            "producto": prod_dict, 
            "cantidad": item.cantidad,
            "precio_unitario": precio_final, 
            "personalizacion": item.personalizacion
        })
        total += precio_final * item.cantidad
        
    return {"items": items_res, "total": total}

@router.post("/items")
def agregar(item_in: schemas.CarritoItemCreate, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    if not carrito:
        carrito = models.Carrito(usuario_id=user.id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)

    # Si es personalizado o tiene precio custom
    if item_in.personalizacion or item_in.precio_custom:
        db.add(models.CarritoItem(
            carrito_id=carrito.id, 
            producto_id=item_in.producto_id,
            cantidad=item_in.cantidad, 
            personalizacion=item_in.personalizacion,
            precio_guardado=item_in.precio_custom # Guardamos el precio del B10
        ))
    else:
        # Producto normal, intentamos agrupar
        existe = db.query(models.CarritoItem).filter(
            models.CarritoItem.carrito_id == carrito.id,
            models.CarritoItem.producto_id == item_in.producto_id,
            models.CarritoItem.personalizacion == None
        ).first()
        if existe: existe.cantidad += item_in.cantidad
        else: db.add(models.CarritoItem(carrito_id=carrito.id, producto_id=item_in.producto_id, cantidad=item_in.cantidad))
    
    db.commit()
    return {"mensaje": "Agregado"}

@router.delete("/items/{item_id}")
def borrar(item_id: int, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    item = db.query(models.CarritoItem).join(models.Carrito).filter(
        models.CarritoItem.id == item_id, models.Carrito.usuario_id == user.id
    ).first()
    if not item: raise HTTPException(404)
    db.delete(item)
    db.commit()
    return {"mensaje": "Borrado"}

@router.delete("/")
def vaciar(user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    carrito = db.query(models.Carrito).filter(models.Carrito.usuario_id == user.id).first()
    if carrito:
        db.query(models.CarritoItem).filter(models.CarritoItem.carrito_id == carrito.id).delete()
        db.commit()
    return {"mensaje": "Vaciado"}