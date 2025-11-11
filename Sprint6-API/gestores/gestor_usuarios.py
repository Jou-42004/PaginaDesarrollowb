# En: gestores/gestor_usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from modelos import schemas
from typing import List

# --- Dependencias de Seguridad (simuladas por ahora) ---
async def get_usuario_actual():
    print("Obteniendo usuario actual (simulación)")
    return schemas.Usuario(
        id="user-uuid-123",
        nombre="Usuario de Prueba",
        rut="12.345.678-9",
        email="test@test.com",
        estado=schemas.EstadoUsuario.ACTIVO
    )
# --------------------------------------------------------

# !!!!! ESTA ES LA LÍNEA QUE FALTA O NO SE GUARDÓ !!!!!
router = APIRouter(
    prefix="/auth", # Prefijo para autenticación
    tags=["Usuarios y Autenticación"]
)

# --- Endpoint para B01: Registro de Usuario ---
@router.post("/registro", response_model=schemas.Usuario)
async def registrar_usuario(usuario_data: schemas.UsuarioCreate):
    print(f"Registrando al usuario: {usuario_data.email}")
    nuevo_usuario = schemas.Usuario(
        id="user-uuid-456",
        nombre=usuario_data.nombre,
        rut=usuario_data.rut,
        email=usuario_data.email,
        telefono=usuario_data.telefono,
        estado=schemas.EstadoUsuario.PENDIENTE
    )
    return nuevo_usuario

# --- Endpoint para B02: Inicio de Sesión ---
@router.post("/token", response_model=schemas.Token)
async def login_para_token(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    print(f"Intento de login para: {email}")

    if email == "test@test.com" and password == "123":
        usuario_simulado = await get_usuario_actual()
        access_token = "simulated-jwt-token-for-" + email

        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "usuario": usuario_simulado
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

# --- Endpoint para B03: Cambio de Contraseña ---
@router.post("/cambiar-password")
async def cambiar_password(
    data: schemas.CambioPassword,
    usuario_actual: schemas.Usuario = Depends(get_usuario_actual)
):
    print(f"Usuario {usuario_actual.email} cambiando contraseña.")
    return {"mensaje": "Contraseña actualizada correctamente."}

# Endpoint para obtener el perfil del usuario (protegido)
@router.get("/me", response_model=schemas.Usuario)
async def read_users_me(usuario_actual: schemas.Usuario = Depends(get_usuario_actual)):
    return usuario_actual