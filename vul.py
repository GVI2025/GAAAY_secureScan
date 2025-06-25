import os
import subprocess
import pickle
import hashlib
import random

# ⚠️ Faille 1 : utilisation de subprocess avec shell=True (injection possible)
def list_files(path):
    command = f"ls {path}"
    return subprocess.call(command, shell=True)


# ⚠️ Faille 3 : utilisation de MD5 (algorithme cryptographique obsolète)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# ⚠️ Faille 2 : désérialisation dangereuse avec pickle (exécution de code arbitraire)
def load_data_from_file(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data

# ⚠️ Faille 4 : génération de token avec random (non sécurisé)
def generate_token():
    return str(random.random())