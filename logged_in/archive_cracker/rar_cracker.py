# from brute import brute
# from .rarfile import RarWrongPassword, RarFile
# from logged_in.archive_cracker import rarfile
import rarfile
import os
from tempfile import gettempdir
from shutil import rmtree
from datetime import datetime
import logging
from pebble import ProcessPool
import glob
from itertools import product
import random
import time

class Rar:
    def __init__(self, file_path):
        self.file_path = file_path
        self.timestamp = datetime.now().timestamp()
        self.export_path = gettempdir() + f"/upload/{int(self.timestamp)}"
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
            logging.info(f"[FILE] Creating temp export directory. Is {self.export_path} created - {str(os.path.exists(self.export_path))}")

    def clear_file(self, file_path=None):
        try:
            if not file_path is None and os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"[FILE] Deleting temp export file. Does {file_path} exist after delete - {str(os.path.exists(file_path))}")
            rmtree(self.export_path)
            logging.info(f"[FILE] Deleting temp export directory. Does {self.export_path} exist after delete - {str(os.path.exists(self.export_path))}")
        except:
            pass

    def extractFile(self, rFile, password):
        try:
            rFile.setpassword(str(password))
            rFile.extractall(self.export_path, pwd=password)
            return True
        except:
            return False
    
    def fromDictionary(self, dictName):
        with open(dictName, "r", encoding="ISO-8859-1") as f:
            for word in f:
                yield word.strip().strip('\n')


    def check_rar(self, dict_path):
        #dict_path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'dict.txt')
        logging.info(f"[RAR] Cracking rar with dict {dict_path}")
        dname = self.fromDictionary(dict_path)
        try:
            with rarfile.RarFile(self.file_path) as zr:
                try:
                    if not zr.needs_password():
                        zr.close()
                        self.clear_file(self.file_path)
                        return 'EMPTY_PASSWORD'
                except Exception as e:
                    logging.error(f"[RAR] Not an empty password:  {e}")
                    pass
                for line in dname:
                    found = self.extractFile(zr, line)
                    if found == True:
                        self.clear_file(self.file_path)
                        return line
            logging.info(f"[RAR] Cracking rar with with dict {dict_path} not succeded")
            self.clear_file()
            return None
        except FileNotFoundError:
            self.clear_file()
            pass

    def brute_crack(self):
        logging.info(f"[RAR] Cracking rar with brute force")
        ALPHABET = "abcdefghijklmtnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=[]{}|\\:~<>?"
        min_pas_len = 1
        max_pas_len = 5
        try:
            for i in range(min_pas_len,max_pas_len+1):
                # ALPHABET = ''.join(random.sample(ALPHABET,len(ALPHABET))) # shuffle alphabet 
                listPass = product(ALPHABET, repeat=i)
                with rarfile.RarFile(self.file_path) as zr:
                    try:
                        if not zr.needs_password():
                            zr.close()
                            self.clear_file(self.file_path)
                            return 'EMPTY_PASSWORD'
                    except RuntimeError as e:
                        logging.error(f"[RAR] Not an empty password: {e}")
                        pass
                    for line in listPass:
                        line = ''.join(line)
                        found = self.extractFile(zr, line)
                        if found == True:
                            self.clear_file(self.file_path)
                            return line
            logging.info(f"[RAR] Cracking rar with with brute force not succeded")
            self.clear_file()
            return None
        except FileNotFoundError as e:
            self.clear_file()
            pass


def crack_rar(file_path):
    logging.info('[RAR] Decrypting rar file')
    dict_txt_files = glob.glob(rf"./logged_in/archive_cracker/dictionaries/*.txt") # Lista słówników z folderu
    if len(dict_txt_files) == 0:
        logging.error('[RAR] Dict not found')
        exit(1)
    future_list = []
    with ProcessPool(max_workers=2, max_tasks=1000) as pool:
        future_list.append(pool.schedule(Rar(file_path).brute_crack))
        time.sleep(0.3)
        for dict_path in dict_txt_files:
            future_list.append(pool.schedule(Rar(file_path).check_rar, args=(dict_path,)))
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
    


if __name__ == '__main__':
    print(crack_rar('./test.rar'))
    # r = Rar('./test.rar')
    # print(r.brute_crack())