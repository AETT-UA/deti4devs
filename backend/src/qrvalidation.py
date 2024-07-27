import os
from hashlib import sha256
import hmac
import time
import base64


validity = 3600 # seconds (int)

k = os.urandom(32)


def sign(data: str) -> str:
    hmac_sha256 = hmac.new(k, digestmod=sha256)
    hmac_sha256.update(data.encode())
    t = int(time.time())
    expiration = t + validity
    expiration = expiration.to_bytes(4, byteorder='big')
    hmac_sha256.update(expiration)
    hash = hmac_sha256.digest()
    # xor the first 16 bytes with the last 16 bytes
    hash = bytes([a ^ b for a, b in zip(hash[:16], hash[16:])])
    # base85 encode the hash
    signature = base64.b85encode(expiration + hash)
    return signature.decode()


def verify(data: str) -> bool:
    if len(data) < 25:
        return False
    
    signature = base64.b85decode(data[-25:].encode())
    expiration = int.from_bytes(signature[:4], byteorder='big')
    if expiration < time.time():
        return False
    
    msg = data[:-25]
    hmac_sha256 = hmac.new(k, digestmod=sha256)
    hmac_sha256.update(msg.encode())
    hmac_sha256.update(signature[:4])
    hash = hmac_sha256.digest()
    hash = bytes([a ^ b for a, b in zip(hash[:16], hash[16:])])
    return hash == signature[4:]


def encodeQr(data: str) -> str:
    return data + sign(data)


def decodeQr(data: str) -> str:
    if verify(data):
        return data[:-25]
    return None


if __name__ == "__main__":
    signed_msg = sign("Hello World")
    print(signed_msg)
    print(verify(signed_msg))
    signed_msg = signed_msg[:-1] + "A" # tamper with the message
    print(verify(signed_msg))
    