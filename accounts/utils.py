import pyotp
import qrcode
import base64
from io import BytesIO

def generate_totp_secret():
    """Genera una clave secreta aleatoria en Base32."""
    return pyotp.random_base32()

def get_totp_qr_code(username, secret):
    """
    Toma el usuario y la clave secreta, y genera un código QR 
    en formato Base64 para mostrarlo directamente en la web.
    """
    totp = pyotp.TOTP(secret)
    # Crea el enlace estándar que leen las apps de autenticación
    provisioning_uri = totp.provisioning_uri(
        name=username, 
        issuer_name="UQ HealthShield"
    )

    # Dibuja el código QR
    qr = qrcode.make(provisioning_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    
    # Lo convierte a texto (Base64) para no tener que guardar la imagen en el disco duro
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{qr_base64}"

def verify_totp(secret, token):
    """Verifica si el código de 6 dígitos que metió el usuario es correcto."""
    totp = pyotp.TOTP(secret)
    return totp.verify(token)