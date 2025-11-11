# En: main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos TODOS nuestros gestores (routers)
from gestores import gestor_usuarios
from gestores import gestor_productos
from gestores import gestor_pedidos
from gestores import gestor_facturacion
from gestores import gestor_admin

app = FastAPI(
    title="Fit Express API",
    description="Backend completo para Fit Express basado en diagramas UX.",
    version="1.0.0"
)

# --- CONFIGURACIÓN DE CORS ---
# Vital para que tu frontend (HTML/JS) pueda hablar con esta API
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "null", # Necesario si abres el B01-RegistroUsuario.html como archivo
    # "https://tu-dominio.com" # Cuando lo subas a producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUIR LOS ROUTERS ---
# Aquí conectamos todos los gestores a la aplicación principal
app.include_router(gestor_usuarios.router)
app.include_router(gestor_productos.router)
app.include_router(gestor_pedidos.router)
app.include_router(gestor_facturacion.router)
app.include_router(gestor_admin.router)


# --- Endpoint Raíz ---
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Fit Express."}