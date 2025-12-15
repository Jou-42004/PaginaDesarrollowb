from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import bcrypt 
from backend import models, schemas, database
from backend.dependencies import SECRET_KEY, ALGORITHM, get_user_from_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registro(user_in: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # Validar existencia previa
    user_exist = db.query(models.Usuario).filter(models.Usuario.email == user_in.email).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya está registrado."
        )
    
    # Preparar datos del usuario
    user_data = user_in.dict()
    plain_password = user_data.pop("password") 
    hashed_pw = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Crear instancia
    nuevo_user = models.Usuario(**user_data, hashed_password=hashed_pw)
    
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    
    # Crear carrito
    carrito = models.Carrito(usuario_id=nuevo_user.id)
    db.add(carrito)
    db.commit()
    
    return {"mensaje": "Usuario creado exitosamente", "id": nuevo_user.id}

@router.post("/token", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == form.username).first()
    
    if not user or not bcrypt.checkpw(form.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {"sub": user.email}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer", "usuario": user}

# ---ENDPOINT PARA RESTABLECER CONTRASEÑA ---
@router.put("/restablecer-password")
def restablecer_password(datos: schemas.PasswordReset, db: Session = Depends(database.get_db)):
    # 1. Buscar usuario
    user = db.query(models.Usuario).filter(models.Usuario.email == datos.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="El correo no está registrado")
    
    # 2. Encriptar nueva contraseña
    hashed_pw = bcrypt.hashpw(datos.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 3. Guardar en BD
    user.hashed_password = hashed_pw
    db.commit()
    
    return {"mensaje": "Contraseña actualizada exitosamente"}

@router.get("/me", response_model=schemas.UsuarioOut)
def me(user: models.Usuario = Depends(get_user_from_token)):
    return user

@router.put("/perfil", response_model=schemas.UsuarioOut)
def actualizar_perfil(
    datos: schemas.UsuarioUpdate, 
    user: models.Usuario = Depends(get_user_from_token), 
    db: Session = Depends(database.get_db)
):
    update_data = datos.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user