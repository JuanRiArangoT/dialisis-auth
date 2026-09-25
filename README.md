# dialisis-auth

Microservicio de autenticación para la plataforma **Diálisis**, desarrollado con **Python, FastAPI y Auth0**.

El servicio centraliza los procesos de autenticación, gestión de credenciales y validación de identidad de los usuarios.

---

## Características

* Registro de usuarios.
* Inicio de sesión.
* Validación de tokens JWT.
* Renovación de tokens mediante refresh token.
* Cierre de sesión.
* Recuperación de contraseña.
* Cambio de contraseña.
* Verificación de correo electrónico.
* Consulta del usuario autenticado.
* Actualización del documento de identidad.
* Integración con Auth0.
* Ejecución mediante Docker.
* Arquitectura Hexagonal.

---

## Tecnologías

* Python 3.13+
* FastAPI
* Pydantic
* Pydantic Settings
* Auth0
* PyJWT
* HTTPX
* uv
* Docker
* pytest
* Ruff
* mypy

---

## Arquitectura

El proyecto utiliza **Arquitectura Hexagonal (Ports and Adapters)**.

```text
                    ┌─────────────────────┐
                    │       Cliente       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI HTTP    │
                    │   Inbound Adapter   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Use Cases      │
                    │     Application     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        Ports        │
                    │     Application     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Auth0 Adapter   │
                    │   Outbound Adapter  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Auth0         │
                    └─────────────────────┘
```

### Estructura

```text
src/auth/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── exceptions/
│   └── services/
│
├── application/
│   ├── dtos/
│   ├── ports/
│   ├── use_cases/
│   └── exceptions/
│
├── adapters/
│   ├── inbound/
│   │   └── http/
│   │       ├── dependencies/
│   │       ├── routes/
│   │       └── schemas/
│   │
│   └── outbound/
│       └── auth0/
│
└── infrastructure/
    └── config/
```

La comunicación sigue el flujo:

```text
HTTP Route
    ↓
Use Case
    ↓
Application Port
    ↓
Auth0 Adapter
    ↓
Auth0
```

---

## API

La API se expone por defecto en:

```text
http://localhost:8000
```

### Health Check

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok",
  "service": "auth-microservice"
}
```

---

### Registrar usuario

```http
POST /auth/register
```

Permite registrar un nuevo usuario mediante Auth0.

---

### Iniciar sesión

```http
POST /auth/login
```

Autentica al usuario y retorna los tokens correspondientes.

Respuesta exitosa:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "refresh_token": "...",
  "id_token": "..."
}
```

---

### Renovar token

```http
POST /auth/refresh
```

Permite obtener un nuevo access token utilizando un refresh token válido.

---

### Cerrar sesión

```http
POST /auth/logout
```

Revoca el refresh token utilizado durante la sesión.

---

### Recuperar contraseña

```http
POST /auth/password/forgot
```

Envía al usuario el proceso de recuperación de contraseña mediante Auth0.

---

### Cambiar contraseña

```http
POST /auth/password/change
```

Permite al usuario autenticado cambiar su contraseña.

Requiere:

```http
Authorization: Bearer <access_token>
```

---

### Actualizar documento

```http
PATCH /auth/users/{user_id}/document
```

Actualiza la información relacionada con el documento del usuario.

---

### Usuario autenticado

```http
GET /auth/me
```

Retorna la información del usuario asociado al access token.

Requiere:

```http
Authorization: Bearer <access_token>
```

---

## Autenticación

La autenticación utiliza **Auth0** como proveedor de identidad.

El flujo general es:

```text
Usuario
   │
   ▼
dialisis-auth
   │
   ▼
Auth0
   │
   ├── Autenticación
   ├── Usuarios
   ├── Contraseñas
   ├── Verificación de correo
   └── Tokens
```

Los access tokens son tokens **JWT** firmados por Auth0.

El microservicio valida:

* Firma del token.
* Emisor (`issuer`).
* Audiencia (`audience`).
* Algoritmo de firma.
* Información requerida del usuario.

---

## Verificación de correo

Los usuarios registrados deben verificar su dirección de correo electrónico antes de iniciar sesión.

El registro utiliza:

```text
verify_email = true
```

Además, Auth0 utiliza un **Post Login Action** para impedir el inicio de sesión de usuarios cuyo correo aún no haya sido verificado.

Cuando un usuario no verificado intenta iniciar sesión, la API responde:

```http
403 Forbidden
```

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_AUDIENCE=https://your-domain.auth0.com/api/v2/
AUTH0_API_AUDIENCE=https://api.dialisis.local
AUTH0_DB_CONNECTION=Username-Password-Authentication
```

**No subir `.env` al repositorio.**

El proyecto utiliza `.env.example` como referencia para las variables requeridas.

---

## Instalación local

### Requisitos

* Python 3.13+
* uv
* Auth0 configurado

Instalar dependencias:

```bash
uv sync
```

Ejecutar el servicio:

```bash
uv run uvicorn auth.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

La documentación interactiva de FastAPI estará disponible en:

```text
http://localhost:8000/docs
```

---

## Docker

Construir la imagen:

```bash
docker compose build
```

Levantar el servicio:

```bash
docker compose up -d
```

Consultar el estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f auth
```

Detener el servicio:

```bash
docker compose down
```

El contenedor utiliza un healthcheck sobre:

```text
GET /health
```

---

## Configuración de Auth0

Para ejecutar correctamente el servicio se requiere configurar en Auth0:

* Application.
* Management API.
* API para `dialisis`.
* Database Connection.
* Password Realm.
* Refresh Token Grant.
* Allow Offline Access.
* Email Provider.
* Email Verification.
* Post Login Action para validar el correo.

El servicio utiliza Auth0 Management API para determinadas operaciones administrativas relacionadas con los usuarios.

---

## Documentación interactiva

Con el servicio ejecutándose, FastAPI proporciona:

### Swagger UI

```text
http://localhost:8000/docs
```

### OpenAPI

```text
http://localhost:8000/openapi.json
```

---

## Desarrollo

Ejecutar Ruff:

```bash
uv run ruff check .
```

Ejecutar mypy:

```bash
uv run mypy src
```

Ejecutar pruebas:

```bash
uv run pytest
```

---

## Repositorio

El código fuente se encuentra en:

`JuanRiArangoT/dialisis-auth`