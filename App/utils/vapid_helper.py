import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

def pem_to_base64url(pem_public_key):
    """
    Convert PEM public key to base64url format for browser consumption
    """
    # Remove PEM headers and decode
    pem_lines = pem_public_key.strip().split('\n')
    pem_data = ''.join(pem_lines[1:-1])  # Remove BEGIN/END lines
    
    # Decode the base64 PEM data
    der_data = base64.b64decode(pem_data)
    
    # Load the public key
    public_key = serialization.load_der_public_key(der_data)
    
    # Get the raw public key bytes (uncompressed format)
    raw_key = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    # Convert to base64url (remove padding and replace chars)
    base64url_key = base64.urlsafe_b64encode(raw_key).decode('utf-8').rstrip('=')
    
    return base64url_key

def get_vapid_public_key_base64url():
    """
    Get the VAPID public key in base64url format for frontend use
    """
    from django.conf import settings
    
    pem_key = settings.VAPID_PUBLIC_KEY
    return pem_to_base64url(pem_key)
