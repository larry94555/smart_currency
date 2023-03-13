from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Final
from cryptography.hazmat.primitives import hashes
import os
from cryptography.hazmat.primitives import serialization
import socket

def create_keys(path):
    privateKey, publicKey = generate_private_and_public_keys()
    privateKeyFile = get_private_key_filename(path)
    publicKeyFile = get_public_key_filename(path)
    create_path_if_needed(path)
    write_bytes_to_file(privateKey, privateKeyFile)
    write_bytes_to_file(publicKey, publicKeyFile)
    return (privateKey, publicKey) 

def create_path_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

CURVE: Final = ec.SECP256K1()
SIGNATURE_ALGORITHM: Final = ec.ECDSA(hashes.SHA256())
MAX_PORT: Final = 65535

def generate_private_and_public_keys():
    curve = ec.SECP256K1()
    privateKey = ec.generate_private_key(curve)
    serializedPrivateKey = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    publicKey = privateKey.public_key()
    serializedPublicKey = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return (serializedPrivateKey, serializedPublicKey)

def get_keys(path):
    if not os.path.exists(path):
        return (None, None)
    privateKeyFile = get_private_key_filename(path)
    publicKeyFile = get_public_key_filename(path)
    return (get_private_key_from_pem_file(privateKeyFile),
            get_public_key_from_pem_file(publicKeyFile)) 

def get_private_key_filename(path):
    return f"{path}/node.private.key.pem"

def get_private_key_from_pem_file(privateKeyFile):
    privateKeyBytes = read_bytes_from_file(privateKeyFile)
    return serialization.load_pem_private_key(
        privateKeyBytes,
        password=None,
        backend=default_backend()
    )

def get_public_key_filename(path):
    return f"{path}/node.public.key.pem"
    
def get_public_key_from_pem_file(publicKeyFile):
    publicKeyBytes = read_bytes_from_file(publicKeyFile)
    publicKey = serialization.load_pem_public_key(publicKeyBytes)
    return publicKey.public_bytes(serialization.Encoding.X962,
                                  serialization.PublicFormat.CompressedPoint).hex()

def read_bytes_from_file(fileWithPath):
    with open(f"{fileWithPath}", "rb") as byteFile:
        return byteFile.read()

def write_bytes_to_file(bytesToWrite, fileWithPath):
    with open(f"{fileWithPath}", "wb") as byteFile:
        byteFile.write(bytesToWrite)
