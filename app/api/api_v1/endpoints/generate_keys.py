from typing import Any, List, Dict, Optional
from fastapi import APIRouter

from app import crud, schemas
from app.api import deps
from app.core.config import settings
from app.core import security
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

router = APIRouter()


@router.get("/", response_model=Dict)
async def generate_keys() -> Any:
    """
    Generate public and private keys
    """
    key_pair = security.generate_private_public_key_pair()

    return key_pair


@router.get("/test-encrypt", response_model=Dict)
async def encrypt_info(msg: str) -> Any:
    """
    Encryt message test

    """
    private_key = security.get_private_key()
    public_key = security.get_public_key()
    print("=============KEYS============")
    # print(private_key)
    # print(public_key)
    # Encrypt a message using the public key
    # message = msg.encode('utf-8')
    message = msg.encode('utf-8')
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # Decrypt the encrypted message using the private key
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    out = {
        "msg": message,
        "encrypted": encrypted,
        "decrypt": decrypted
    }
    print(out)

    return {"mesesage": message}
