from fastapi import APIRouter
from app.api.api_v1.endpoints import list_tables, login, users, connectors_types, save_connection, generate_keys

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    connectors_types.router, prefix="/connectors-types", tags=["connectors-types"])
api_router.include_router(
    save_connection.router, prefix="/save-connection", tags=["save-connections"])
api_router.include_router(
    generate_keys.router, prefix="/generate-keys", tags=["generate-keys"])
api_router.include_router(
    list_tables.router, prefix="/list-metadata", tags=["generate-metadata"])
