# src/auth/adapters/outbound/auth0/auth0_service.py
from typing import Any

import httpx
from fastapi import HTTPException, status

from ....application.dtos import (
    RegisterUserCommand,
    UpdateDocumentCommand,
    UserOutputDTO,
)
from ....application.ports.authentication import AuthenticationPort
from ....infrastructure.config.settings import settings


class Auth0ServiceAdapter(AuthenticationPort):
    def __init__(self):
        self._domain = settings.AUTH0_DOMAIN
        self._client_id = settings.AUTH0_CLIENT_ID
        self._client_secret = settings.AUTH0_CLIENT_SECRET
        self._audience = settings.AUTH0_AUDIENCE
        self._connection = settings.AUTH0_DB_CONNECTION
        self._base_url = f"https://{self._domain}"

    async def _get_management_token(self) -> str:
        url = f"{self._base_url}/oauth/token"
        payload = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "audience": self._audience,
            "grant_type": "client_credentials"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Error obteniendo token de Management API: {response.text}"
                )
            return response.json().get("access_token")

    async def register(self, command: RegisterUserCommand) -> UserOutputDTO:
        token = await self._get_management_token()
        url = f"{self._base_url}/api/v2/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Requisito 3 de la guía: full_name en el campo estándar 'name'
        payload = {
            "connection": self._connection,
            "email": command.email,
            "password": command.password,
            "name": command.full_name,
            "verify_email": False
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            if response.status_code not in (200, 201):
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error al registrar usuario en Auth0: {response.text}"
                )
            data = response.json()
            return UserOutputDTO(
                user_id=data["user_id"],
                email=data["email"],
                full_name=data.get("name", "")
            )

    async def update_document_metadata(self, command: UpdateDocumentCommand) -> dict[str, Any]:
        token = await self._get_management_token()
        url = f"{self._base_url}/api/v2/users/{command.user_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Requisito 3 de la guía: Guardar en user_metadata
        payload = {
            "user_metadata": {
                "tipo_documento": command.tipo_documento,
                "numero_documento": command.numero_documento
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=payload, headers=headers, timeout=10.0)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error actualizando user_metadata en Auth0: {response.text}"
                )
            return response.json().get("user_metadata", {})