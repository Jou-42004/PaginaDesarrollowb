from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
# AGREGAR admin AQUI
from .routers import auth, catalogo, carrito, pedidos, facturacion, admin 

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(catalogo.router)
app.include_router(carrito.router)
app.include_router(pedidos.router)
app.include_router(facturacion.router)
app.include_router(admin.router) 


@app.get("/")
def home():
    return {"mensaje": "API Fit Express Lista"}