def get_hash_type(hash):
    if hash is None:
        pass
    elif type(hash) == str:
        if len(hash) == 32:
                return 'md5'
        elif len(hash) == 40:
            return 'sha1'
        elif len(hash) == 64:
            return 'sha256'
        elif len(hash) == 96:
            return 'sha384'
        elif len(hash) == 128:
            return 'sha512'
        else:
            return False