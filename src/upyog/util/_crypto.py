import upyog as upy
from upyog.util.string import safe_encode
from upyog.util.eject  import ejectable

@ejectable(deps = ["safe_encode"])
def sha256(s):
    import hashlib
    encoded = safe_encode(s)
    return hashlib.sha256(encoded).hexdigest()