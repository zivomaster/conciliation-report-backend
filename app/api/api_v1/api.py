from fastapi import APIRouter
from app.api.api_v1.endpoints import list_tables, login, users, connectors_types, save_connection, generate_keys

api_router = APIRouter()
api_router.include_router(login.router, tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(
    connectors_types.router, prefix="/connectors-types", tags=["ConnectorTypes"])
api_router.include_router(
    save_connection.router, prefix="/save-connection", tags=["SaveConnections"])
api_router.include_router(
    generate_keys.router, prefix="/generate-keys", tags=["GenerateKeys"])
api_router.include_router(
    list_tables.router, prefix="/tables", tags=["Select/List Tables"])
