from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/catalogo", tags=["Catálogo"])

@router.get("/productos", response_model=List[schemas.ProductoOut])
def listar(db: Session = Depends(database.get_db)):
    productos = db.query(models.Producto).all()
    for p in productos:
        p.macros = {"kcal": p.kcal, "p": p.proteina, "f": p.grasas, "c": p.carbs}
    return productos