import hashlib

def hash_fun(hash_string):
    hash_obj = hashlib.md5(hash_string.encode())
    return hash_obj.hexdigest()