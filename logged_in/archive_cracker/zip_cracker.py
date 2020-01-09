import zipfile
import os
from tempfile import gettempdir
from shutil import rmtree, copyfile
from datetime import datetime
import logging
from random import shuffle
import threading 
import time
from pebble import ProcessPool
import glob
from itertools import product
import random

running = None
class Zip():
    def __init__(self, file_path):
        self.file_path = file_path
        self.timestamp = datetime.now().timestamp()
        self.export_path = gettempdir() + f"/upload/{int(self.timestamp)}"
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
            logging.info(f"[FILE] Creating temp export directory. Is {self.export_path} created - {str(os.path.exists(self.export_path))}")

    def extractFile(self, zFile, password):
        try:
            zFile.setpassword(password.encode())
            zFile.extractall(self.export_path)
            return True
        except:
            return False

    def clear_file(self, file_path=None):
        try:
            if not file_path is None and os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"[FILE] Deleting temp export file. Does {file_path} exist after delete - {str(os.path.exists(file_path))}")
            rmtree(self.export_path)
            logging.info(f"[FILE] Deleting temp export directory. Does {self.export_path} exist after delete - {str(os.path.exists(self.export_path))}")
        except:
            pass

    def fromDictionary(self, dictName):
        with open(dictName, "r", encoding="ISO-8859-1") as f:
            for word in f:
                yield word.strip()

    def check_zip(self, dict_path):
        logging.info(f"[ZIP] Cracking zip with dict {dict_path}")
        dname = self.fromDictionary(dict_path)
        try:
            with zipfile.ZipFile(self.file_path) as zf:
                try:
                    if zf.testzip() == None:
                        zf.close()
                        self.clear_file(self.file_path)
                        return 'EMPTY_PASSWORD'
                except RuntimeError as e:
                    pass
                for line in dname:
                    found = self.extractFile(zf, line)
                    if found == True:
                        self.clear_file(self.file_path)
                        return line
            logging.info(f"[ZIP] Cracking zip with dict {dict_path} not succeded")
            self.clear_file()
            return None
        except FileNotFoundError:
            pass

    def brute_crack(self):
        logging.info(f"[ZIP] Cracking zip with brute force")
        ALPHABET = "abcdefghijklmtnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=[]{}|\\:~<>?"
        min_pas_len = 1
        max_pas_len = 5
        try:
            for i in range(min_pas_len,max_pas_len+1):
                # ALPHABET = ''.join(random.sample(ALPHABET,len(ALPHABET))) # shuffle alphabet 
                listPass = product(ALPHABET, repeat=i)
                with zipfile.ZipFile(self.file_path) as zf:
                    try:
                        if zf.testzip() == None:
                            zf.close()
                            self.clear_file(self.file_path)
                            return 'EMPTY_PASSWORD'
                    except RuntimeError as e:
                        pass
                    for line in listPass:
                        line = ''.join(line)
                        found = self.extractFile(zf, line)
                        if found == True:
                            self.clear_file(self.file_path)
                            return line
            logging.info(f"[ZIP] Cracking zip with brute force not succeded")
            self.clear_file()
            return None
        except FileNotFoundError:
            pass

def crack_zip(file_path):
    logging.info('[ZIP] Decrypting zip file')
    dict_txt_files = glob.glob(rf"./logged_in/archive_cracker/dictionaries/*.txt") # Lista słówników z folderu
    if len(dict_txt_files) == 0:
        logging.error('[ZIP] Dict not found')
        exit(1)
    future_list = []
    with ProcessPool(max_workers=4, max_tasks=99999) as pool:
        future_list.append(pool.schedule(Zip(file_path).brute_crack))
        for dict_path in dict_txt_files:
            future_list.append(pool.schedule(Zip(file_path).check_zip, args=(dict_path,)))
            time.sleep(0.3)
        found = False
        # from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
        # done, not_done = wait(thread_list, timeout=6, return_when=FIRST_COMPLETED) # Alternative
        while not found:
            if len(future_list) == 0:
                break
            for f in future_list:
                if f.done():
                    ret = f.result()
                    if ret is None:
                        f.cancel()
                        future_list.remove(f)
                        continue
                    else:
                        found = True
                        for _f in future_list: # Clear all processes left
                            _f.cancel()
                            future_list.remove(_f)
                        pool.stop()
                        return ret
                else:
                    continue
    



# if __name__=="__main__":
#     print("Running")
#     # z = Zip("./test.zip")
#     # ret = z.brute_crack()
#     ret = crack_zip("./test.zip")
#     print(ret)