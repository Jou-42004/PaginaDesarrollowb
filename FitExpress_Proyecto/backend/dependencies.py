from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import database, models

# Configuración JWT
# Nota: En producción, estos valores deberían cargarse desde variables de entorno
SECRET_KEY = "FITEXPRESS_SECRETO"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # Definir excepción común para errores de credenciales
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Buscar usuario en BD
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    
    if user is None:
        raise credentials_exception
        
    return user