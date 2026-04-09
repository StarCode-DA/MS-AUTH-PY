from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.config import settings

# Contexto de hashing con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora
# Limite de bcrypt
MAX_BCRYPT_LENGTH = 72  # bcrypt solo acepta hasta 72 bytes
# Esquema de seguridad HTTP Bearer
bearer = HTTPBearer()

# ================================
# Funciones de seguridad
# ================================

def hash_password(password: str) -> str:
    """
    Hashea una contraseña aplicando truncamiento a 72 bytes
    """
    pwd_to_hash = password[:MAX_BCRYPT_LENGTH]
    return pwd_context.hash(pwd_to_hash)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña aplicando truncamiento a 72 bytes
    """
    pwd_to_verify = plain_password[:MAX_BCRYPT_LENGTH]
    return pwd_context.verify(pwd_to_verify, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Crea un token JWT con expiración de ACCESS_TOKEN_EXPIRE_MINUTES
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer)
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
def hash_answer(answer: str) -> str:
    return pwd_context.hash(answer.lower().strip())

def verify_answer(plain_answer: str, hashed_answer: str) -> bool:
    return pwd_context.verify(plain_answer.lower().strip(), hashed_answer)