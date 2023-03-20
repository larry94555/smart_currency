import asyncio
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Final
from cryptography.hazmat.primitives import hashes
import operator
import os
from cryptography.hazmat.primitives import serialization
import socket
import sys

def bytes_to_bit_string(bytes):
    print(f"util::bytes_to_bit_string: bytes:{bytes}")
    result="Empty"
    try:
        bits = [bin(int(byte,16))[2:].rjust(8, '0') for byte in bytes]
        #print(f"util::bytes_to_bit_string: bits: {bits}")
        result = "".join(bits)
    except:
        type, value, traceback = sys.exc_info()
        print(f"util::bytes_to_bit_string: type: {type}, value: {value}, traceback: {traceback}")
      
    return result

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

async def gather_dict(dic):
    cors = list(dic.values())
    results = await asyncio.gather(*cors)
    return dict(zip(dic.keys(), results))

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
    result =  serialization.load_pem_private_key(
        privateKeyBytes,
        password=None,
        backend=default_backend()
    )
    return result

def get_public_key_filename(path):
    return f"{path}/node.public.key.pem"
    
def get_public_key_from_pem_file(publicKeyFile):
    publicKeyBytes = read_bytes_from_file(publicKeyFile)
    publicKey = serialization.load_pem_public_key(publicKeyBytes)
    result = publicKey.public_bytes(serialization.Encoding.X962,
                                  serialization.PublicFormat.CompressedPoint).hex()
    return result

def read_bytes_from_file(fileWithPath):
    print(f"util:read_bytes_fromfile: {fileWithPath}")
    with open(f"{fileWithPath}", "rb") as byteFile:
        result = byteFile.read()
        byteFile.close()
    return result

def shared_prefix(args):
    i = 0
    while i < min(map(len, args)):
        if len(set(map(operator.itemgetter(i), args))) != 1:
            break
        i += 1
    return args[0][:i]

def write_bytes_to_file(bytesToWrite, fileWithPath):
    print(f"util::write_bytes_to_file: {fileWithPath}")
    with open(f"{fileWithPath}", "wb") as byteFile:
        results=byteFile.write(bytesToWrite)
        byteFile.close()
    return results 
    
