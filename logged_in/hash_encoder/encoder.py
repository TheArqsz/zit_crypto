import hashlib
from database.models import Hash, db
def encode(text, mode):
    if mode == 'sha256':
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
        h = Hash(mode, digest, text)
        db.session.add(h)
        try:
            db.session.commit()
        except Exception as e:
            pass
        return digest
    if mode == 'md5':
        digest = hashlib.md5(text.encode('utf-8')).hexdigest()
        h = Hash(mode, digest, text)
        db.session.add(h)
        try:
            db.session.commit()
        except Exception as e:
            pass
        return digest
    if mode == 'sha1':
        digest = hashlib.sha1(text.encode('utf-8')).hexdigest()
        h = Hash(mode, digest, text)
        db.session.add(h)
        try:
            db.session.commit()
        except Exception as e:
            pass
        return digest
    if mode == 'sha384':
        digest = hashlib.sha384(text.encode('utf-8')).hexdigest()
        h = Hash(mode, digest, text)
        db.session.add(h)
        try:
            db.session.commit()
        except Exception as e:
            pass
        return digest
    if mode == 'sha512':
        digest = hashlib.sha512(text.encode('utf-8')).hexdigest()        
        h = Hash(mode, digest, text)
        db.session.add(h)
        try:
            db.session.commit()
        except Exception as e:
            pass
        return digest