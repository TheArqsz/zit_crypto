from .zip_cracker import crack_zip
from .rar_cracker import crack_rar
from .sevenz_cracker import crack_zip as crack_sevenz
import logging
import magic 
import copy
from tempfile import gettempdir
from base64 import b64encode
import os

def handle_file(file_path, file_mime):
    if file_mime == 'application/zip' or file_mime == 'application/x-zip-compressed':
        ret = crack_zip(file_path)
        logging.info(f"[ZIP] Cracked: {ret}")
        return ret
    elif file_mime == 'application/x-rar-compressed' or file_mime == 'application/x-rar':
        ret = crack_rar(file_path)
        logging.info(f"[RAR] Cracked: {ret}")
        return ret   
    elif file_mime == 'application/x-7z-compressed':
        ret = crack_sevenz(file_path)
        logging.info(f"[7z] Cracked: {ret}")
        return ret
    else:
        logging.info(f"[FILE] Mime type {file_mime} was not correct")
        return 

def get_allowed_mime_types():
    return [
        "application/zip",
        "application/x-zip-compressed",
        "application/x-rar-compressed",
        "application/x-rar",
        "application/x-7z-compressed"
    ]

def get_buffer_mime_type(buffer):
    return magic.from_buffer(buffer.stream.read(1024), mime=True)


def get_file_mime_type(file_path):
    return magic.from_file(file_path, mime=True)

def clear_file(file_path):
    import os
    if os.path.exists(file_path):
        os.remove(file_path)
    logging.info(f"[FILE] Deleting temp file. Does {file_path} exist - {str(os.path.exists(file_path))}")