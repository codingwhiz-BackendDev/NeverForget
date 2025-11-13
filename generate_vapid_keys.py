from cryptography.hazmat.primitives import serialization
import base64

pem_public_key = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+6biIJfHoMb2k67gNVSTEV7aVw5f
xRs0Vq3al0j8k6j0bpRGe6tXuDqTqnVujlZGyV3zjBy7wpfZGHjYKAdX1w==
-----END PUBLIC KEY-----"""

public_key = serialization.load_pem_public_key(pem_public_key.encode('utf-8'))

# Convert to uncompressed point bytes
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# Base64URL encode (remove padding)
public_key_base64url = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip('=')
print("Base64URL public key for frontend:", public_key_base64url)
