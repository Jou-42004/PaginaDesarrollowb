from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .routers import auth, catalogo, carrito, pedidos, facturacion, admin

# Inicializar tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

# Configuración de la aplicación
app = FastAPI(
    title="Fit Express API",
    description="Backend para gestión de e-commerce de comida saludable (Caso 19).",
    version="1.0.0"
)

# Configuración de seguridad (CORS)
# Permite que el frontend (HTML/JS) se comunique con este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas (Controllers)
app.include_router(auth.router)
app.include_router(catalogo.router)
app.include_router(carrito.router)
app.include_router(pedidos.router)
app.include_router(facturacion.router)
app.include_router(admin.router)

# Endpoint de verificación
@app.get("/", tags=["General"])
def root():
    return {
        "sistema": "Fit Express API", 
        "estado": "En línea", 
        "documentacion": "/docs"
    }