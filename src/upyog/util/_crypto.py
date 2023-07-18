import upyog as upy

def sha256(s):
    import hashlib
    encoded = upy.safe_encode(s)
    return hashlib.sha256(encoded).digest()