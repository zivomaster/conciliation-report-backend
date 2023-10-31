from datetime import datetime, timedelta
from typing import Any, Union, Dict

from jose import jwt
from passlib.context import CryptContext
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from app.services.AWS_handled_files import s3_upload, s3_download


from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
BUCKET_PATH_KEYS = "development/development/key-pair/"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_private_public_key_pair() -> Dict:
    # Generate a private-public key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    # Serialize the keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    save_priv_key = s3_upload(contents=private_pem,
                              key=settings.PRIVATE_KEY_PEM_NAME + '.pem',
                              path=BUCKET_PATH_KEYS)
    save_pub_key = s3_upload(contents=public_pem,
                             key=settings.PUBLIC_KEY_PEM_NAME + '.pem',
                             path=BUCKET_PATH_KEYS)
    return {
        "message": {
            "private_key": save_priv_key,
            "public_key": save_pub_key
        },
        "status": 200
    }


def get_private_key():
    # Download private key from S3
    response = s3_download(
        settings.PRIVATE_KEY_PEM_NAME+'.pem', BUCKET_PATH_KEYS)
    private_key_data = response['Body'].read()
    # Deserialize private key
    # For example, to print the keys
    private_key = serialization.load_pem_private_key(
        private_key_data, password=None)
    print("Private Key:", private_key)
    return private_key


def get_public_key():
    # Download private key from S3
    response = s3_download(
        settings.PUBLIC_KEY_PEM_NAME+'.pem', BUCKET_PATH_KEYS)
    public_key_data = response['Body'].read()
    # Deserialize private key
    public_key = serialization.load_pem_public_key(public_key_data)
    print("Public Key:", public_key)
    return public_key
