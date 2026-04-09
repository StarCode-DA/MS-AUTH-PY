# 🔐 Eclipse Bar — Microservicio de Autenticación (MS-AUTH-PY)

Microservicio encargado de la autenticación y autorización del sistema **Eclipse Bar**. Gestiona el login, recuperación de contraseña y validación de tokens JWT.

---

## 📋 Tabla de contenido

- [Tecnologías](#tecnologías)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
- [Seguridad](#seguridad)
- [Modelos de base de datos](#modelos-de-base-de-datos)
- [Correr con Docker](#correr-con-docker)

---

## 🛠 Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) — Framework web
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM para base de datos
- [PostgreSQL](https://www.postgresql.org/) — Base de datos
- [Passlib + bcrypt](https://passlib.readthedocs.io/) — Hashing de contraseñas
- [python-jose](https://python-jose.readthedocs.io/) — Generación y validación de JWT
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — Gestión de configuración
- [Uvicorn](https://www.uvicorn.org/) — Servidor ASGI

---

## ✅ Requisitos previos

- Python >= 3.11
- PostgreSQL corriendo (o usar Docker)
- Base de datos `eclipsebar_db` inicializada con `init.sql`

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd MS-AUTH-PY

# Instalar dependencias
pip install -r requirements.txt

# Correr el servidor
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🔧 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/eclipsebar_db
SECRET_KEY=super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> ⚠️ **Importante:** Cambia `SECRET_KEY` por una clave segura antes de desplegar en producción.

---

## 📁 Estructura del proyecto

```
src/
├── models/
│   ├── usuario.py          # Modelo principal de usuarios
│   ├── mesero.py           # Modelo de meseros (para obtener nombre en /me)
│   ├── cajero.py           # Modelo de cajeros (para obtener nombre en /me)
│   └── administrador.py    # Modelo de administradores (para obtener nombre en /me)
├── routers/
│   └── auth.py             # Endpoints de autenticación
├── schemas/
│   └── auth.py             # Schemas Pydantic (request/response)
├── utils/
│   └── security.py         # JWT, hashing y verificación
├── config.py               # Configuración con Pydantic Settings
├── database.py             # Conexión a la base de datos
└── main.py                 # Punto de entrada de la aplicación
```

---

## 📡 Endpoints

Base URL: `http://localhost:8001`

| Método | Endpoint                   | Auth | Descripción                                      |
|--------|----------------------------|------|--------------------------------------------------|
| POST   | `/auth/login`              | ❌   | Iniciar sesión, retorna token JWT                |
| POST   | `/auth/forgot-password`    | ❌   | Restablecer contraseña con pregunta de seguridad |
| GET    | `/auth/security-question`  | ❌   | Obtener pregunta de seguridad por email          |
| GET    | `/auth/me`                 | ✅   | Obtener datos del usuario autenticado            |

### POST `/auth/login`
```json
// Request
{ "email": "admin@eclipsebar.com", "password": "Admin1234" }

// Response
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "rol": "administrador",
  "sede_id": null
}
```

### POST `/auth/forgot-password`
```json
// Request
{
  "email": "admin@eclipsebar.com",
  "security_answer": "respuesta",
  "new_password": "NuevaPass123"
}

// Response
{ "message": "Password updated successfully" }
```

### GET `/auth/security-question?email=...`
```json
// Response
{ "security_question": "¿Cuál es el nombre de tu mascota?" }
```

### GET `/auth/me`
```json
// Response
{
  "id": 1,
  "email": "admin@eclipsebar.com",
  "rol": "administrador",
  "sede_id": null,
  "nombre": "Carlos Admin"
}
```

---

## 🔒 Seguridad

### JWT
- Los tokens se generan con `python-jose` usando el algoritmo `HS256`.
- Expiran en **60 minutos** por defecto.
- Contienen: `sub` (id del usuario), `email`, `rol`, `sede_id`.
- Se validan en cada endpoint protegido mediante `HTTPBearer`.

### Contraseñas
- Se hashean con **bcrypt** usando `passlib`.
- bcrypt acepta máximo **72 bytes** — las contraseñas se truncan antes de hashear para evitar comportamientos inesperados.
- Las respuestas de seguridad se normalizan (minúsculas + sin espacios) antes de hashear.

### Validación de contraseña
La contraseña debe cumplir:
- Mínimo 8 caracteres
- Al menos una mayúscula
- Al menos una minúscula
- Al menos un número

---

## 🗄️ Modelos de base de datos

Este microservicio accede a las siguientes tablas:

| Tabla             | Uso                                                  |
|-------------------|------------------------------------------------------|
| `usuarios`        | Login, validación de credenciales y estado activo    |
| `meseros`         | Obtener nombre del perfil en `/me`                   |
| `cajeros`         | Obtener nombre del perfil en `/me`                   |
| `administradores` | Obtener nombre del perfil en `/me`                   |

> Los modelos de `meseros`, `cajeros` y `administradores` están duplicados en este microservicio porque comparte la misma base de datos con `MS-USER-PY` pero son servicios independientes.

---

## 🐳 Correr con Docker

```bash
# Construir imagen
docker build -t eb-auth .

# Correr contenedor
docker run -p 8001:8001 --env-file .env eb-auth
```

O usar el Docker Compose del repositorio `INFRA-EB-DK`:

```bash
cd INFRA-EB-DK/compose
docker compose up -d auth
```

---

## 📖 Documentación automática

FastAPI genera documentación automática disponible en:

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`
