# Diálisis Auth

Microservicio de autenticación para la plataforma **Diálisis**, desarrollado con Python y FastAPI bajo los principios de **Arquitectura Hexagonal**.

El servicio centraliza la autenticación, gestión de credenciales y operaciones relacionadas con la identidad de los usuarios utilizando **Auth0** como proveedor de identidad.

## Responsabilidades

`dialisis-auth` se encarga principalmente de:

* Registro de usuarios en Auth0.
* Inicio de sesión.
* Renovación de tokens.
* Cierre de sesión.
* Recuperación de contraseña.
* Cambio de contraseña.
* Verificación de correo electrónico.
* Validación de tokens JWT.
* Consulta de la identidad del usuario autenticado.
* Actualización de información relacionada con el documento de identidad.
* Integración con Auth0 Management API.

La información de negocio y persistencia propia del usuario es responsabilidad de `dialisis-users`.

## Arquitectura

El proyecto implementa **Arquitectura Hexagonal (Ports and Adapters)**.

```text
                         ┌─────────────────────┐
                         │       Cliente       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI HTTP     │
                         │    Inbound Adapter  │
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
                         │     Auth0 Adapter    │
                         │   Outbound Adapter  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        Auth0        │
                         └─────────────────────┘
```

El flujo principal sigue:

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

## Estructura

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

### Responsabilidades por capa

| Capa              | Responsabilidad                                           |
| ----------------- | --------------------------------------------------------- |
| Domain            | Entidades, objetos de valor y reglas propias del dominio. |
| Application       | Casos de uso, DTOs, puertos y excepciones de aplicación.  |
| Adapters Inbound  | Exposición de la API HTTP mediante FastAPI.               |
| Adapters Outbound | Comunicación con Auth0.                                   |
| Infrastructure    | Configuración y componentes técnicos.                     |

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
* Docker Compose
* Pytest
* Ruff
* mypy

## API

La API expone los endpoints relacionados con autenticación e identidad.

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

### Registrar usuario

```http
POST /auth/register
```

Registra un nuevo usuario mediante Auth0.

### Iniciar sesión

```http
POST /auth/login
```

Autentica al usuario y retorna los tokens correspondientes.

Respuesta de ejemplo:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "refresh_token": "...",
  "id_token": "..."
}
```

### Renovar token

```http
POST /auth/refresh
```

Obtiene un nuevo access token utilizando un refresh token válido.

### Cerrar sesión

```http
POST /auth/logout
```

Permite cerrar la sesión y revocar el refresh token utilizado.

### Recuperar contraseña

```http
POST /auth/password/forgot
```

Inicia el proceso de recuperación de contraseña mediante Auth0.

### Cambiar contraseña

```http
POST /auth/password/change
Authorization: Bearer <access_token>
```

Permite al usuario autenticado cambiar su contraseña.

### Actualizar documento

```http
PATCH /auth/users/{user_id}/document
Authorization: Bearer <access_token>
```

Actualiza la información relacionada con el documento del usuario.

### Usuario autenticado

```http
GET /auth/me
Authorization: Bearer <access_token>
```

Obtiene información relacionada con la identidad del usuario asociado al access token.

## Autenticación

Auth0 actúa como proveedor de identidad de la plataforma.

El flujo general es:

```text
┌──────────────┐
│    Cliente   │
└──────┬───────┘
       │
       ▼
┌────────────────────┐
│   dialisis-auth    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│       Auth0        │
│                    │
│ • Autenticación    │
│ • Usuarios         │
│ • Contraseñas      │
│ • Tokens           │
│ • Email            │
└────────────────────┘
```

Los access tokens utilizados por la plataforma son **JWT** emitidos por Auth0.

El servicio valida, entre otros aspectos:

* Firma del token.
* Emisor (`issuer`).
* Audiencia (`audience`).
* Algoritmo de firma.
* Información requerida del usuario.

## Verificación de correo

Los usuarios registrados deben verificar su dirección de correo electrónico.

El registro utiliza la configuración:

```text
verify_email = true
```

Además, Auth0 utiliza un **Post Login Action** para impedir el inicio de sesión de usuarios cuyo correo electrónico todavía no haya sido verificado.

Cuando un usuario no verificado intenta iniciar sesión, el servicio responde:

```http
403 Forbidden
```

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

### Variables

| Variable            | Descripción                                                          |
| ------------------- | -------------------------------------------------------------------- |
| AUTH0_DOMAIN        | Dominio del tenant de Auth0.                                         |
| AUTH0_CLIENT_ID     | Identificador de la aplicación de Auth0.                             |
| AUTH0_CLIENT_SECRET | Secreto de la aplicación.                                            |
| AUTH0_AUDIENCE      | Audiencia utilizada para las operaciones correspondientes con Auth0. |
| AUTH0_API_AUDIENCE  | Audiencia de la API de Diálisis.                                     |
| AUTH0_DB_CONNECTION | Conexión de base de datos utilizada para los usuarios.               |

**Importante:** no subir `.env`, credenciales, secretos ni tokens al repositorio.

El proyecto utiliza `.env.example` como referencia para las variables requeridas.

## Instalación local

### Requisitos

* Python 3.13+
* uv
* Cuenta/configuración de Auth0 válida.

### Instalar dependencias

```powershell
uv sync
```

### Ejecutar el servicio

```powershell
uv run uvicorn auth.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

## Docker

Construir la imagen:

```powershell
docker compose build
```

Iniciar el servicio:

```powershell
docker compose up -d
```

Verificar el estado:

```powershell
docker compose ps
```

Consultar logs:

```powershell
docker compose logs -f auth
```

Detener los servicios:

```powershell
docker compose down
```

El contenedor utiliza el endpoint:

```text
GET /health
```

como health check.

## Configuración de Auth0

Para ejecutar correctamente el servicio se requiere configurar en Auth0 los componentes necesarios para la autenticación de Diálisis.

Entre ellos:

* Application.
* Management API.
* API de Diálisis.
* Database Connection.
* Password Realm.
* Refresh Token Grant.
* Allow Offline Access.
* Email Provider.
* Email Verification.
* Post Login Action para validación del correo.

El microservicio utiliza Auth0 Management API para determinadas operaciones administrativas relacionadas con los usuarios.

## Relación con otros microservicios

La arquitectura de Diálisis separa la autenticación de la información de negocio del usuario.

```text
                    ┌───────────────────┐
                    │      Cliente      │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │  dialisis-auth  │       │ dialisis-users  │
        │                 │       │                 │
        │ Autenticación   │       │ Usuarios        │
        │ Credenciales    │       │ Perfil          │
        │ Tokens          │       │ Roles           │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 ▼                         ▼
             ┌───────┐              ┌─────────────┐
             │ Auth0 │              │ PostgreSQL  │
             └───────┘              └─────────────┘
```

`dialisis-auth` es responsable de la identidad y las credenciales.

`dialisis-users` es responsable de la información propia del usuario dentro de la plataforma, incluyendo su perfil y `role_id`.

## Documentación interactiva

FastAPI genera automáticamente la documentación OpenAPI.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

### OpenAPI

```text
http://localhost:8000/openapi.json
```

## Pruebas

Ejecutar todos los tests:

```powershell
uv run pytest
```

## Calidad de código

Ejecutar Ruff:

```powershell
uv run ruff check .
```

Corregir automáticamente los problemas compatibles:

```powershell
uv run ruff check . --fix
```

Ejecutar mypy:

```powershell
uv run mypy src
```

## Estado del proyecto

Actualmente el microservicio cuenta con:

* Registro de usuarios.
* Inicio de sesión.
* Renovación de tokens.
* Cierre de sesión.
* Recuperación de contraseña.
* Cambio de contraseña.
* Verificación de correo electrónico.
* Validación de tokens JWT.
* Consulta del usuario autenticado.
* Actualización del documento de identidad.
* Integración con Auth0.
* Arquitectura Hexagonal.
* Pruebas automatizadas.
* Ruff.
* mypy.
* Contenerización mediante Docker.
* Documentación OpenAPI mediante FastAPI.

## Repositorio

El código fuente se encuentra en:

```text
JuanRiArangoT/dialisis-auth
```
