import os
import base64
import streamlit as st
from zoneinfo import ZoneInfo
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from bbdd import get_client

# ========================
# FUNCIONES DE CIFRADO
# ========================
password = os.getenv("CLAVE_AES").encode()

salt_b64 = os.getenv("SALT")
salt = base64.b64decode(salt_b64)

def cifrar_aes(mensaje, clave):
    padder = sym_padding.PKCS7(128).padder()
    mensaje_padded = padder.update(mensaje) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(mensaje_padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def descifrar_aes(token_b64, clave):
    data = base64.b64decode(token_b64.encode())
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    mensaje_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()
    mensaje = unpadder.update(mensaje_padded) + unpadder.finalize()

    return mensaje

def derivar_clave(password, salt):
    if isinstance(password, str):
        password = password.encode()  # Convertir a bytes si viene como string
    if isinstance(salt, str):
        salt = base64.b64decode(salt)  # Decodificar si es base64 string

    # Derivar la clave AES con PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,        # clave de 32 bytes para AES-256
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    clave = kdf.derive(password)  # clave derivada para usar en AES
    return clave


def obtener_siguiente_id():
    client = get_client()
    response = client.table("Historial").select("id").execute()
    
    if response.data:
        # Obtener el máximo ID actual
        ids = [fila["id"] for fila in response.data if "id" in fila]
        if ids:
            return max(ids) + 1
    return 1  # Si no hay registros, empezar por 1

def registrar_resultado(mensaje):
    try:
        clave = derivar_clave(password, salt)

        # Obtener hora actual en UTC
        now_utc = datetime.now(tz=ZoneInfo("UTC"))
        # Convertir a hora local (por ejemplo, Madrid)
        now_local = now_utc.astimezone(ZoneInfo("Europe/Madrid"))
        mensaje = now_local.strftime("%Y-%m-%dT%H:%M:%S") + " - " + mensaje
        mensaje_cifrado = cifrar_aes(mensaje.encode(), clave)
        id_registro = obtener_siguiente_id()
        client = get_client()
        data = {
            "id": id_registro,
            "resultados": mensaje_cifrado
        }
        response = client.table("Historial").insert(data).execute()

        # Manejo de errores (opcional, ya lo tienes)
        if hasattr(response, "error") and response.error is not None:
            # manejar error
            pass
        else:
            # éxito
            pass


    except Exception:
        pass

def mostrar_resultados():
    clave = derivar_clave(password, salt)
    resultados = []
    client = get_client()
    response = client.table("Historial").select("*").execute()  # Obtener todos los campos

    if response.data:
        for fila in response.data:
            mensaje_cifrado = fila.get("resultados", "")
            id_registro = fila.get("id", None)  # Por si quieres mostrarlo también
            if mensaje_cifrado:
                try:
                    mensaje_descifrado = descifrar_aes(mensaje_cifrado, clave).decode()
                except Exception:
                    mensaje_descifrado = "[Error al descifrar]"
            else:
                mensaje_descifrado = "[Sin mensaje]"
            
            resultados.append({
                "id": id_registro,
                "mensaje": mensaje_descifrado
            })

    return resultados


