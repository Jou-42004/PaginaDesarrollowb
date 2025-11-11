# En: gestores/gestor_productos.py
from fastapi import APIRouter
from modelos import schemas
from typing import List

router = APIRouter(
    prefix="/catalogo",
    tags=["Productos y Catálogo"]
)

# --- Datos de ejemplo (simulando la BD) ---
db_macros = {"kcal": 420, "p": 24, "f": 12, "c": 54}
db_productos = [
    schemas.Producto(id="prod-1", nombre="Bowl Quinoa", macros=db_macros, disponible=True, precio_base=7990, imagen_url="img.png"),
    schemas.Producto(id="prod-2", nombre="Bowl Proteico", macros=db_macros, disponible=False, precio_base=8990, imagen_url="img.png"),
    schemas.Producto(id="prod-3", nombre="Snack Almendras", macros=db_macros, disponible=True, precio_base=1990, imagen_url="img.png")
]
db_promos = [
    schemas.Promocion(id="promo-1", nombre="Combo Proteico", prioridad=schemas.PrioridadPromo.ALTA, descuento_porc=15),
    schemas.Promocion(id="promo-2", nombre="Bowl Vegano + Postre", prioridad=schemas.PrioridadPromo.MEDIA, descuento_porc=10)
]

# --- Endpoint para B05: Catálogo ---
@router.get("/productos", response_model=List[schemas.Producto])
async def obtener_catalogo():
    """
    Devuelve todos los productos para el B05-CatalogoMacros.
    """
    print("Devolviendo catálogo de productos...")
    return db_productos

# --- Endpoint para B06: Filtro (simulado) ---
@router.post("/productos/filtrar", response_model=List[schemas.Producto])
async def filtrar_productos(filtro: schemas.Filtro):
    """
    Recibe los filtros del B06 y devuelve productos.
    Aquí iría la lógica de búsqueda en la BD.
    """
    print(f"Filtrando productos por: {filtro.dict()}")
    # Simulación: solo devolvemos los disponibles
    return [p for p in db_productos if p.disponible]

# --- Endpoint para B08: Promociones ---
@router.get("/promociones", response_model=List[schemas.Promocion])
async def obtener_promociones():
    """
    Devuelve las promociones vigentes para B08.
    """
    print("Devolviendo promociones...")
    return db_promos