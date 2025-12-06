from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import bcrypt 
from backend import models, schemas, database
from backend.dependencies import SECRET_KEY, ALGORITHM, get_user_from_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro")
def registro(user: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # 1. Verificar si el email ya existe
    if db.query(models.Usuario).filter(models.Usuario.email == user.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 2. Encriptar contraseña
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 3. Crear el usuario con TODOS los datos del formulario B01
    nuevo_user = models.Usuario(
        nombre=user.nombre, 
        email=user.email,
        hashed_password=hashed_pw,
        rut=user.rut, 
        telefono=user.telefono,
        direccion=user.direccion, 
        comuna=user.comuna, 
        region=user.region
    )
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    
    # 4. Crear carrito vacío asociado al usuario
    db.add(models.Carrito(usuario_id=nuevo_user.id))
    db.commit()
    
    return {"mensaje": "Usuario creado exitosamente"}

@router.post("/token", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == form.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    if not bcrypt.checkpw(form.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "usuario": user}

@router.get("/me", response_model=schemas.UsuarioOut)
def me(user: models.Usuario = Depends(get_user_from_token)):
    return user

@router.put("/perfil", response_model=schemas.UsuarioOut)
def actualizar_perfil(datos: schemas.UsuarioUpdate, user: models.Usuario = Depends(get_user_from_token), db: Session = Depends(database.get_db)):
    if datos.nombre: user.nombre = datos.nombre
    if datos.telefono: user.telefono = datos.telefono
    if datos.direccion: user.direccion = datos.direccion
    if datos.comuna: user.comuna = datos.comuna
    if datos.region: user.region = datos.region
    
    db.commit()
    db.refresh(user)
    return user