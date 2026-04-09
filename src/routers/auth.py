from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.usuario import Usuario
from src.models.mesero import Mesero
from src.models.cajero import Cajero
from src.models.administrador import Administrador
from src.utils.security import verify_password, create_access_token, hash_password, hash_answer, verify_answer, get_current_user
from src.schemas.auth import LoginRequest, TokenResponse, ForgotPasswordRequest, ForgotPasswordResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Endpoint para login
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.activo:
        raise HTTPException(status_code=403, detail="Inactive user. Contact administrator")
    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "rol": user.rol,
        "sede_id": user.sede_id
    })
    return {
        "access_token": token,
        "rol": user.rol,
        "sede_id": user.sede_id
    }

# Endpoint para recuperar contraseña
@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not user.activo:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.security_question or not user.security_answer_hash:
        raise HTTPException(status_code=400, detail="This user does not have a security question set up")
    if not verify_answer(data.security_answer, user.security_answer_hash):
        raise HTTPException(status_code=401, detail="Incorrect security answer")
    validar_password(data.new_password)
    user.password_hash = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

# Función para validar la contraseña
def validar_password(password: str):
    if (len(password) < 8 or
        not any(c.isupper() for c in password) or
        not any(c.islower() for c in password) or
        not any(c.isdigit() for c in password)):
        raise HTTPException(
            status_code=400,
            detail="The password must have a minimum of: 8 characters, one uppercase letter, one lowercase letter, and one number"
        )

# Endpoint para obtener la pregunta de seguridad
@router.get("/security-question")
def get_security_question(email: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not user.security_question:
        raise HTTPException(status_code=404, detail="User not found or security question not set")
    return {"security_question": user.security_question}

# Endpoint para obtener los datos del usuario actual
@router.get("/me")
def me(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(Usuario).filter(Usuario.id == int(current_user.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.rol == "mesero":
        perfil = db.query(Mesero).filter(Mesero.usuario_id == user.id).first()
    elif user.rol == "cajero":
        perfil = db.query(Cajero).filter(Cajero.usuario_id == user.id).first()
    else:
        perfil = db.query(Administrador).filter(Administrador.usuario_id == user.id).first()
    return {
        "id": user.id,
        "email": user.email,
        "rol": user.rol,
        "sede_id": user.sede_id,
        "nombre": perfil.nombre if perfil else user.email
    }