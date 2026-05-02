import json
import os
from core.crypto import derive_key, encrypt, decrypt
from core.models import Entry
from dataclasses import asdict

def create_vault(key, path, salt):
    empty = []
    json_data = json.dumps(empty)
    encoded = json_data.encode()
    blob = encrypt(encoded, key)
    dati = salt + blob
    with open(path, "wb") as f:
        f.write(dati)

def save_vault(entries, key, path):
    with open(path, "rb") as f:
        content = f.read()
    salt = content[:16]
    file = []  
    for e in entries:
        d = asdict(e)
        d["id"] = str(d["id"])
        file.append(d)
    json_data = json.dumps(file)
    encoded = json_data.encode()
    blob = encrypt(encoded, key)
    dati = salt + blob
    with open(path, "wb") as f:
        f.write(dati)

def load_vault(key, path):
    with open(path, "rb") as f:
        content = f.read()
    blob = content[16:]
    pw = decrypt(blob, key)
    decoded = pw.decode()
    json_list = json.loads(decoded)
    listE = [Entry(**d) for d in json_list]
    return listE