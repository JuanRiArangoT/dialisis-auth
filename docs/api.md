# API — dialisis-auth

Documentación de los endpoints expuestos por `dialisis-auth`.

Base URL local:

```text
http://localhost:8000
```

---

## Autenticación

Los endpoints protegidos requieren un access token JWT emitido por Auth0.

Header:

```http
Authorization: Bearer <access_token>
```

Los endpoints que requieren autenticación están identificados en cada sección.

---

# Health Check

## `GET /health`

Verifica que el microservicio esté disponible.

### Autenticación

No requiere autenticación.

### Response `200`

```json
{
  "status": "ok",
  "service": "auth-microservice"
}
```

---

# Registro

## `POST /auth/register`

Registra un nuevo usuario en Auth0.

### Autenticación

No requiere autenticación.

### Request

```json
{
  "email": "usuario@example.com",
  "password": "Password123!",
  "full_name": "Juan Pérez"
}
```

### Campos

| Campo       | Tipo   | Requerido | Descripción                    |
| ----------- | ------ | --------: | ------------------------------ |
| `email`     | string |        Sí | Correo electrónico del usuario |
| `password`  | string |        Sí | Contraseña                     |
| `full_name` | string |        Sí | Nombre completo                |

### Response `201`

Retorna la información básica del usuario registrado.

```json
{
  "user_id": "auth0|123456789",
  "email": "usuario@example.com",
  "full_name": "Juan Pérez"
}
```

---

# Inicio de sesión

## `POST /auth/login`

Autentica un usuario mediante Auth0.

### Autenticación

No requiere access token.

### Request

```json
{
  "email": "usuario@example.com",
  "password": "Password123!"
}
```

### Response `200`

```json
{
  "access_token": "<access_token>",
  "token_type": "Bearer",
  "expires_in": 86400,
  "refresh_token": "<refresh_token>",
  "id_token": "<id_token>"
}
```

### Errores

#### `401 Unauthorized`

Credenciales inválidas.

```json
{
  "detail": "Invalid credentials."
}
```

#### `403 Forbidden`

El correo electrónico del usuario no ha sido verificado.

```json
{
  "detail": "Please verify your email before logging in."
}
```

---

# Renovación del token

## `POST /auth/refresh`

Obtiene un nuevo access token utilizando un refresh token válido.

### Autenticación

No requiere access token.

### Request

```json
{
  "refresh_token": "<refresh_token>"
}
```

### Response `200`

```json
{
  "access_token": "<new_access_token>",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### Errores

#### `401 Unauthorized`

El refresh token no es válido o ya no puede utilizarse.

```json
{
  "detail": "Invalid refresh token."
}
```

---

# Cierre de sesión

## `POST /auth/logout`

Revoca el refresh token utilizado durante la sesión.

### Autenticación

No requiere access token.

### Request

```json
{
  "refresh_token": "<refresh_token>"
}
```

### Response `200`

```json
{
  "message": "Logout successful."
}
```

### Errores

#### `401 Unauthorized`

El refresh token no es válido.

```json
{
  "detail": "Invalid refresh token."
}
```

---

# Recuperación de contraseña

## `POST /auth/password/forgot`

Solicita el proceso de recuperación de contraseña.

Auth0 envía el correo correspondiente al usuario.

### Autenticación

No requiere autenticación.

### Request

```json
{
  "email": "usuario@example.com"
}
```

### Response `200`

```json
{
  "message": "Password recovery email sent."
}
```

---

# Cambio de contraseña

## `POST /auth/password/change`

Permite al usuario autenticado cambiar su contraseña.

### Autenticación

Requiere access token.

```http
Authorization: Bearer <access_token>
```

### Request

```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword123!"
}
```

### Campos

| Campo              | Tipo   | Requerido | Descripción       |
| ------------------ | ------ | --------: | ----------------- |
| `current_password` | string |        Sí | Contraseña actual |
| `new_password`     | string |        Sí | Nueva contraseña  |

Las contraseñas deben tener como mínimo 8 caracteres.

### Response `200`

```json
{
  "message": "Password changed successfully."
}
```

### Errores

#### `401 Unauthorized`

La contraseña actual no es válida.

```json
{
  "detail": "Invalid current password."
}
```

---

# Actualización de documento

## `PATCH /auth/users/{user_id}/document`

Actualiza la información del documento de identidad del usuario.

### Autenticación

Requiere access token.

```http
Authorization: Bearer <access_token>
```

### Path Parameter

| Parámetro | Tipo   | Descripción                        |
| --------- | ------ | ---------------------------------- |
| `user_id` | string | Identificador del usuario en Auth0 |

### Request

```json
{
  "tipo_documento": "CC",
  "numero_documento": "1234567890"
}
```

### Response

Retorna la información actualizada del usuario.

---

# Usuario autenticado

## `GET /auth/me`

Obtiene la información del usuario asociado al access token.

### Autenticación

Requiere access token.

```http
Authorization: Bearer <access_token>
```

### Response `200`

```json
{
  "user_id": "auth0|123456789",
  "email": "usuario@example.com",
  "full_name": "Juan Pérez"
}
```

### Errores

#### `401 Unauthorized`

El access token no es válido.

---

# Flujo de autenticación

El flujo principal de autenticación es:

```text
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       │ POST /auth/login
       ▼
┌─────────────────┐
│  dialisis-auth  │
└────────┬────────┘
         │
         │ Password Realm
         ▼
┌─────────────────┐
│      Auth0      │
└────────┬────────┘
         │
         │ Tokens
         ▼
┌─────────────────┐
│  dialisis-auth  │
└────────┬────────┘
         │
         │ Access Token
         ▼
┌─────────────┐
│   Cliente   │
└─────────────┘
```

Posteriormente, el cliente utiliza el access token para acceder a los recursos protegidos de la plataforma.

```text
Cliente
   │
   │ Authorization: Bearer <token>
   ▼
Microservicio
   │
   ▼
Validación JWT
   │
   ├── Token válido ──────► Procesar solicitud
   │
   └── Token inválido ────► 401 Unauthorized
```

---

# Gestión del ciclo de vida de sesión

El ciclo de vida utiliza access tokens y refresh tokens:

```text
Login
  │
  ├── Access Token
  │
  └── Refresh Token
          │
          ▼
       Refresh
          │
          └── Nuevo Access Token
          
          │
          ▼
        Logout
          │
          └── Revocación del Refresh Token
```

---

# Recuperación de contraseña

El flujo de recuperación utiliza Auth0:

```text
Cliente
   │
   │ POST /auth/password/forgot
   ▼
dialisis-auth
   │
   ▼
Auth0
   │
   ▼
Correo de recuperación
   │
   ▼
Usuario
```

---

# Cambio de contraseña

El cambio de contraseña requiere que el usuario esté autenticado:

```text
Cliente
   │
   │ Access Token
   ▼
dialisis-auth
   │
   ├── Valida Access Token
   │
   ├── Valida contraseña actual
   │
   └── Actualiza contraseña
          │
          ▼
        Auth0
```

---

# Verificación de correo

Los usuarios registrados deben verificar su correo electrónico.

El flujo es:

```text
Registro
   │
   ▼
Auth0
   │
   ├── Usuario creado
   │
   └── Correo de verificación
          │
          ▼
       Usuario
          │
          ▼
   Correo verificado
          │
          ▼
       Login
```

Si el correo no está verificado, el login es rechazado:

```http
403 Forbidden
```

---

# Códigos HTTP

| Código | Uso                                              |
| ------ | ------------------------------------------------ |
| `200`  | Operación exitosa                                |
| `201`  | Usuario creado                                   |
| `400`  | Solicitud inválida                               |
| `401`  | Credenciales o token inválido                    |
| `403`  | Usuario no autorizado o correo no verificado     |
| `409`  | Usuario ya existente                             |
| `422`  | Error de validación de datos                     |
| `502`  | Error de comunicación con proveedor de identidad |
| `503`  | Proveedor temporalmente no disponible            |

---

# Documentación OpenAPI

Con el servicio ejecutándose:

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI:

```text
http://localhost:8000/openapi.json
```
