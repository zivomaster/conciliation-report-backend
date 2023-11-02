from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from decouple import config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = config("SECRET_KEY", cast=str)
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    current_file = Path(__file__).resolve()
    BASE_DIR = current_file.parent.parent
    TMP_FILES_STR: str = '/services/tmp_files/'
    # JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173"]
    PROJECT_NAME: str = "CONCILIATION-REPORT"
    # DATABASE CONFIGURATION
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", cast=str)
    POSTGRES_USER: str = config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str)
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str)
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int)
    SQLALCHEMY_DATABASE_URI: str = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # AWS
    AWS_BUCKET_NAME: str = config("AWS_BUCKET_NAME", cast=str)
    AWS_REGION: str = ""
    AWS_ACCESS_KEY_ID: str = config("AWS_ACCESS_KEY_ID", cast=str)
    AWS_SECRET_ACCESS_KEY: str = config("AWS_SECRET_ACCESS_KEY", cast=str)
    BUCKET_PATH_SAVE_CONNECTIONS: str = config(
        "BUCKET_PATH_SAVE_CONNECTIONS", cast=str)
    BUCKET_PATH_KEYS: str = config(
        "BUCKET_PATH_KEYS", cast=str)
    BUCKET_PATH_KEYS_AUTH_CONNECTIONS: str = config(
        "BUCKET_PATH_KEYS_AUTH_CONNECTIONS", cast=str)
    
    BUCKET_PATH_SELECT_CONNECTIONS: str = config(
        "BUCKET_PATH_SELECT_CONNECTIONS", cast=str)
    # KEY-PAIRS
    PRIVATE_KEY_PEM_NAME: str = config("PRIVATE_KEY_PEM_NAME", cast=str)
    PUBLIC_KEY_PEM_NAME: str = config("PUBLIC_KEY_PEM_NAME", cast=str)
    # FILES HANDLED
    SUPPORTED_FILE_TYPES = {
        # 'data:application/json;base64': 'json',
        'data:application/csv;base64': 'csv',
        'data:text/csv;base64': 'csv',
        'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64': 'xlsx',
    }
    # CONNECTIONS HANDLED
    ALLOW_DIALECTS_DB = {
        "PostgreSQL": "postgresql+psycopg2",
        "MySQL": "mysql+pymysql",
        "Oracle": "oracle+cx_oracle",
        "SQLServer": "mssql+pyodbc",
        "MongoDB": "MongoDB",
        "BigQuery": "BigQuery"
    }

    class Config:
        case_sensitive = True


settings = Settings()
