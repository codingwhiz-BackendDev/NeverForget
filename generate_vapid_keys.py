#!/usr/bin/env python3
"""
Script to generate new VAPID keys compatible with pywebpush
Run this script to get new VAPID keys for your Django settings
"""

from py_vapid import Vapid
import base64
from cryptography.hazmat.primitives import serialization

def generate_vapid_keys():
    """Generate new VAPID key pair"""
    vapid = Vapid()
    
    # Generate new key pair
    vapid.generate_keys()
    
    private_key_pem = vapid.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    public_key_pem = vapid.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    # Get base64url public key for frontend
    public_key_bytes = vapid.public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    public_key_base64url = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip('=')
    
    print("=" * 60)
    print("NEW VAPID KEYS FOR DJANGO SETTINGS")
    print("=" * 60)
    print()
    print("Replace these in your Django settings.py:")
    print()
    print("VAPID_PRIVATE_KEY = '''")
    print(private_key_pem.strip())
    print("'''")
    print()
    print("VAPID_PUBLIC_KEY = '''")
    print(public_key_pem.strip())
    print("'''")
    print()
    print("Base64URL Public Key (for frontend verification):")
    print(public_key_base64url)
    print()
    print("=" * 60)
    print("INSTRUCTIONS:")
    print("1. Copy the above keys to your Django settings.py")
    print("2. Delete existing Push Subscriptions in Django admin")
    print("3. Restart your Django server")
    print("4. Test push notifications")
    print("=" * 60)

if __name__ == "__main__":
    generate_vapid_keys()
