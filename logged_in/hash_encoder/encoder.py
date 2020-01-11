import hashlib
from flask import session
from database.models import Hash, db
def encode(text, mode):
    if mode == 'sha256':
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
        remember_to_db(mode, digest, text)
        return digest
    if mode == 'md5':
        digest = hashlib.md5(text.encode('utf-8')).hexdigest()
        remember_to_db(mode, digest, text)
        return digest
    if mode == 'sha1':
        digest = hashlib.sha1(text.encode('utf-8')).hexdigest()
        remember_to_db(mode, digest, text)
        return digest
    if mode == 'sha384':
        digest = hashlib.sha384(text.encode('utf-8')).hexdigest()
        remember_to_db(mode, digest, text)
        return digest
    if mode == 'sha512':
        digest = hashlib.sha512(text.encode('utf-8')).hexdigest()        
        remember_to_db(mode, digest, text)
        return digest

def remember_to_db(mode, hash, plain):
    if session.get("DO_NOT_REMEMBER"):
        return
    else:
        h = Hash(mode, hash, plain)
        db.session.add(h)
        try:
            db.session.commit()
        except Exception as e:
            pass