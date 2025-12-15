from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/catalogo", tags=["Catálogo"])

@router.get("/productos", response_model=List[schemas.ProductoOut])
def get_catalog_products(db: Session = Depends(database.get_db)):
    # Obtener todos los productos, ordenados por ID para consistencia visual
    productos = db.query(models.Producto).order_by(models.Producto.id).all()
    
    # Mapear las columnas individuales de la BD al diccionario 'macros' que espera el Schema
    for p in productos:
        p.macros = {
            "kcal": p.kcal, 
            "p": p.proteina, 
            "f": p.grasas, 
            "c": p.carbs
        }
        
    return productos