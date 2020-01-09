# def is_hash_by_(hash, hash_type):
#     if hash is None:
#         pass
#     elif type(hash) == str:
#         if hash_type == 'md5':
#             if len(hash) == 32:
#                 return True
#         elif hash_type == 'sha1':
#             if len(hash) == 40:
#                 return True
#         elif hash_type == 'sha256':
#             if len(hash) == 64:
#                 return True
#         elif hash_type == 'sha384':
#             if len(hash) == 96:
#                 return True
#         elif hash_type == 'sha512':
#             if len(hash) == 128:
#                 return True
#         else:
#             return False

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