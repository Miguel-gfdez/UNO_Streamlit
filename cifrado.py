from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hashes, padding as sym_padding



# La contraseña la coges de la variable de entorno
password = os.getenv("CLAVE_AES").encode()  # contraseña en bytes

# Salt fijo (mejor guardarlo y usar siempre el mismo para que derive la misma clave)
salt_b64 = os.getenv("SALT")
salt = base64.b64decode(salt_b64)

# Derivar la clave AES con PBKDF2HMAC
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,        # clave de 32 bytes para AES-256
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

clave = kdf.derive(password)  # clave derivada para usar en AES

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

# Ejemplo
texto_original = b"Este es el texto que quiero cifrar"
texto_cifrado = cifrar_aes(texto_original, clave)
print("Texto cifrado:", texto_cifrado)

texto_descifrado = descifrar_aes(texto_cifrado, clave)
print("Texto descifrado:", texto_descifrado.decode())







# def generar_claves_rsa(password: str, ruta_privada: str = "clave_privada.pem", ruta_publica: str = "clave_publica.pem"):
#     private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
#     public_key = private_key.public_key()

#     # Derivar clave de cifrado para la privada con PBKDF2
#     salt = os.urandom(16)
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(), length=32, salt=salt,
#         iterations=100_000, backend=default_backend()
#     )
#     key = kdf.derive(password.encode())

#     encrypted_private_key = private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.BestAvailableEncryption(key)
#     )

#     # Guardar claves
#     with open(ruta_privada, "wb") as f:
#         f.write(salt + encrypted_private_key)
#     with open(ruta_publica, "wb") as f:
#         f.write(public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         ))

# def generar_clave_aes(public_key_path: str, ruta_salida: str = "clave_aes_cifrada.bin"):
#     # Leer clave pública
#     with open(public_key_path, "rb") as f:
#         public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

#     # Generar clave AES aleatoria
#     clave_aes = os.urandom(32)

#     # Cifrar la clave AES con RSA
#     clave_aes_cifrada = public_key.encrypt(
#         clave_aes,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )

#     # Guardar clave AES cifrada en binario
#     with open(ruta_salida, "wb") as f:
#         f.write(clave_aes_cifrada)

# def registrar_resultado_cifrado_hibrido(resultado: str, public_key_path: str, ruta_fichero: str = "Ganadores.txt", ruta_clave_aes: str = "clave_aes_cifrada.bin"):
#     # Leer clave pública
#     with open(public_key_path, 'rb') as f:
#         public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

#     # Generar clave AES y cifrar el mensaje
#     clave_aes = os.urandom(32)
#     iv = os.urandom(16)
#     cipher = Cipher(algorithms.AES(clave_aes), modes.CFB(iv))
#     encryptor = cipher.encryptor()

#     try:
#         with open(ruta_fichero, 'rb') as f:
#             datos_previos = f.read()
#             texto_plano = datos_previos.decode() + resultado + "\n"
#     except FileNotFoundError:
#         texto_plano = resultado + "\n"

#     texto_cifrado = encryptor.update(texto_plano.encode()) + encryptor.finalize()

#     # Cifrar la clave AES con RSA
#     clave_aes_cifrada = public_key.encrypt(
#         clave_aes,
#         padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
#     )

#     # Guardar contenido cifrado (sin incluir clave cifrada)
#     datos_finales = {
#         "iv": base64.b64encode(iv).decode(),
#         "contenido": base64.b64encode(texto_cifrado).decode()
#     }
#     with open(ruta_fichero, 'w') as f:
#         json.dump(datos_finales, f)

#     # Guardar clave cifrada por separado
#     with open(ruta_clave_aes, 'wb') as f:
#         f.write(clave_aes_cifrada)

# def leer_resultados_descifrados(private_key_path: str, password: str, ruta_fichero: str = "Ganadores.txt",
#                                 ruta_clave_aes: str = "clave_aes_cifrada.bin"):
#     # Leer archivo cifrado
#     with open(ruta_fichero, 'r') as f:
#         datos = json.load(f)

#     iv = base64.b64decode(datos["iv"])
#     contenido_cifrado = base64.b64decode(datos["contenido"])

#     # Leer clave AES cifrada
#     with open(ruta_clave_aes, 'rb') as f:
#         clave_cifrada = f.read()

#     # Cargar clave privada con la contraseña
#     with open(private_key_path, 'rb') as f:
#         contenido = f.read()
#         salt = contenido[:16]
#         encrypted_key = contenido[16:]

#         kdf = PBKDF2HMAC(
#             algorithm=hashes.SHA256(), length=32, salt=salt,
#             iterations=100_000, backend=default_backend()
#         )
#         key = kdf.derive(password.encode())

#         private_key = serialization.load_pem_private_key(
#             encrypted_key,
#             password=key,
#             backend=default_backend()
#         )

#     # Descifrar clave AES
#     clave_aes = private_key.decrypt(
#         clave_cifrada,
#         padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
#     )

#     # Descifrar contenido
#     cipher = Cipher(algorithms.AES(clave_aes), modes.CFB(iv))
#     decryptor = cipher.decryptor()
#     texto = decryptor.update(contenido_cifrado) + decryptor.finalize()

#     return texto.decode()

# generar_claves_rsa("hola") # prueba de generación de claves RSA
# generar_clave_aes("clave_publica.pem")

