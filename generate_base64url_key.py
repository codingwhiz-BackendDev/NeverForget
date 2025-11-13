#!/usr/bin/env python3
"""
Convert PEM public key to base64url format for browser
"""

import base64

def pem_to_base64url():
    """Convert PEM public key to base64url format"""
    
    # The PEM public key we just generated
    pem_key = '''-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAELZrGmEf9PLq5C8+Wgim1xgNQ/mry
DDDGlccp3pC2bYKQ/BT9tt/kqud07fqAKCb/9ZDIL08xtCkAUMiCN28WsQ==
-----END PUBLIC KEY-----'''
    
    # Extract the base64 part (remove header, footer, and newlines)
    lines = pem_key.strip().split('\n')
    base64_part = ''.join(lines[1:-1])  # Remove first and last lines
    
    # Convert to base64url format (replace + with -, / with _, remove padding)
    base64url = base64_part.replace('+', '-').replace('/', '_').rstrip('=')
    
    return base64url

if __name__ == "__main__":
    print("Converting PEM public key to base64url format...")
    print("=" * 60)
    
    base64url_key = pem_to_base64url()
    
    print("Base64url Public Key:")
    print("-" * 30)
    print(base64url_key)
    print()
    
    print("=" * 60)
    print("Copy this to your pwa.js applicationServerKey")
    print()
    
    print("Example pwa.js configuration:")
    print("-" * 40)
    print(f"applicationServerKey: this.urlBase64ToUint8Array('{base64url_key}')")
    print()
