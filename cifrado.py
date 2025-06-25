import os
import base64
import streamlit as st
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
password = os.getenv("CLAVE_AES")#.encode()
st.warning(type(password))
st.warning(type(password.encode()))

salt_b64 = os.getenv("SALT")
salt = base64.b64decode(salt_b64)
st.warning(type(salt_b64))
st.warning(type(salt))

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

def registrar_resultado(mensaje):
    st.write(mensaje)
    try:
        clave = derivar_clave(password, salt)
        mensaje = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + " - " + mensaje
        mensaje_cifrado = cifrar_aes(mensaje.encode(), clave)

        client = get_client()
        data = {"resultados": mensaje_cifrado}
        response = client.table("Historial").insert(data).execute()

        # Revisar si hay error
        if hasattr(response, "error") and response.error is not None:
            # st.error(f"Error al insertar: {response.error}")
            pass
        elif response.status_code not in (200, 201):
            # st.error(f"Error al insertar: Código {response.status_code}")
            pass
        else:
            # st.success("Datos guardados correctamente")
            pass

    except Exception as e:
        # print("Error cifrado:", e)
        pass
        # Aquí no mostrar variables sensibles


def mostrar_resultados():
    clave = derivar_clave(password, salt)
    resultados = []
    # Crear cliente de Supabase para conectarse a la base de datos
    client = get_client()
    response = client.table("Historial").select("resultados").execute()

    if response.data:
        for fila in response.data:
            mensaje_cifrado = fila.get("resultados", "")
            if mensaje_cifrado:
                try:
                    mensaje_descifrado = descifrar_aes(mensaje_cifrado, clave)
                    resultados.append(mensaje_descifrado.decode())
                except Exception as e:
                    resultados.append("[Error al descifrar]")
    return resultados

