from pydantic import BaseModel
from typing import Optional

# Datos necesarios para iniciar sesión
class LoginRequest(BaseModel):
    email: str
    password: str
    
# Respuesta que se devuelve al iniciar sesión exitosamente
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    sede_id: Optional[int] = None
    
# Datos necesarios para solicitar un cambio de contraseña    
class ForgotPasswordRequest(BaseModel):
    email: str
    security_answer: str
    new_password: str
    
# Respuesta que se devuelve al solicitar un cambio de contraseña exitosamente
class ForgotPasswordResponse(BaseModel):
    message: str