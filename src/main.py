from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.auth import router as auth_router

# Configuración y base de datos
app = FastAPI(title="MS AUTH")
# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", # dominios que pueden hacer requests
        "http://localhost:5173"
    ],
    allow_credentials=True, # cookies y credenciales
    allow_methods=["*"], # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # headers permitidos
)
# Routers
app.include_router(auth_router)