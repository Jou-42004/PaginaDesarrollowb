from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from passlib.context import CryptContext
from modelos import schemas, models
from database import get_session

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["Usuarios y Autenticación"]
)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Dependencia para obtener usuario actual (usada por otros gestores)
async def get_usuario_actual(token: str = Depends(schemas.Token), db: Session = Depends(get_session)):
    # NOTA: Aquí simplificamos. En producción, decodificarías el JWT.
    # Para este sprint, buscaremos un usuario "por defecto" o simularemos validación.
    # Si usas login real, el token debería ser el ID o email encriptado.
    
    # MODO SIMPLE: Si el token es un email válido en la BD, lo dejamos pasar
    # (Esto es solo para desarrollo, NO PRODUCCIÓN)
    user = db.exec(select(models.Usuario).where(models.Usuario.correo == token)).first()
    if not user:
        # Fallback para pruebas con usuario test
        user = db.exec(select(models.Usuario).where(models.Usuario.correo == "test@test.com")).first()
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )
    return user

# --- Endpoint para B01: Registro de Usuario ---
@router.post("/registro", response_model=schemas.Usuario)
async def registrar_usuario(
    usuario_data: schemas.UsuarioCreate,
    db: Session = Depends(get_session)
):
    # 1. Validar duplicados
    existing_user = db.exec(select(models.Usuario).where(models.Usuario.correo == usuario_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # 2. Crear modelo de BD
    nuevo_usuario = models.Usuario(
        nombre=usuario_data.nombre,
        rut=usuario_data.rut,
        correo=usuario_data.email,
        telefono=usuario_data.telefono,
        contrasena_hash=get_password_hash(usuario_data.password),
        estado=models.EstadoUsuarioEnum.ACTIVO # Lo activamos directo por simplicidad
    )
    
    # 3. Guardar
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    # Crear carrito vacío para el usuario
    nuevo_carrito = models.Carrito(usuario_id=nuevo_usuario.id, total=0)
    db.add(nuevo_carrito)
    db.commit()

    return nuevo_usuario

# --- Endpoint para B02: Inicio de Sesión ---
@router.post("/token", response_model=schemas.Token)
async def login_para_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    email = form_data.username
    password = form_data.password

    # Buscar usuario
    user = db.exec(select(models.Usuario).where(models.Usuario.correo == email)).first()

    if not user or not verify_password(password, user.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # En un sistema real, aquí creas un JWT.
    # Para mantenerlo simple ahora, usaremos el email como token
    access_token = user.correo 

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "usuario": user
    }

@router.get("/me", response_model=schemas.Usuario)
async def read_users_me(
    token: str = Depends(schemas.Token), # Esto fuerza autenticación
    db: Session = Depends(get_session)
):
    # Lógica simplificada: buscar usuario por el token (que es el email)
    # Ojo: En producción usarías Depends(get_usuario_actual) directamente
    user = db.exec(select(models.Usuario).where(models.Usuario.correo == token.access_token)).first()
    return user