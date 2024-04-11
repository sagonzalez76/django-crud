import pyotp
from datetime import datetime, timedelta
import base64
import random
import string


def generate_random_string(length=32):
    # Genera una cadena aleatoria de longitud especificada sin números
    return ''.join(random.choices(string.ascii_letters, k=length))


random_string = generate_random_string(32)

def send_otp():
    
    key = random_string
    totp = pyotp.TOTP(key)
    uri = totp.provisioning_uri(
        name='User',
        issuer_name='Suntic')
    return key, uri

   
    


def to_base64(data):
    return base64.b64encode(data).decode('utf-8')
