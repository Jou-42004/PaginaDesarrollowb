from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from modelos import schemas, models
from database import get_session

router = APIRouter(
    prefix="/catalogo",
    tags=["Productos y Catálogo"]
)

# --- 1. Obtener Catálogo (REAL desde BD) ---
@router.get("/productos", response_model=List[schemas.Producto])
async def obtener_catalogo(db: Session = Depends(get_session)):
    # Busca todos los productos en la tabla Producto
    statement = select(models.Producto)
    productos = db.exec(statement).all()
    return productos

# --- 2. Crear Producto (Para que TÚ los agregues) ---
@router.post("/productos", response_model=schemas.Producto)
async def crear_producto(
    prod_in: schemas.ProductoCreate, 
    db: Session = Depends(get_session)
):
    # 1. Crear Macros
    nuevos_macros = models.Macros(
        kcal=prod_in.kcal,
        p=prod_in.p,
        f=prod_in.f,
        c=prod_in.c
    )
    db.add(nuevos_macros)
    db.commit()
    db.refresh(nuevos_macros)

    # 2. Crear Producto vinculado a esos Macros
    nuevo_producto = models.Producto(
        nombre=prod_in.nombre,
        precio=prod_in.precio,
        disponible=prod_in.disponible,
        imagen_url=prod_in.imagen_url,
        macros_id=nuevos_macros.id
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    
    return nuevo_producto