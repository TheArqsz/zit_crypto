#
#
#   Testing .7z files - currently very slow cause of using system library
#
#

import subprocess
import os
from tempfile import gettempdir
from shutil import rmtree
from datetime import datetime
import logging
from random import shuffle
from pebble import ProcessPool
import glob
from itertools import product
import random
import time

class SevenZip:
    def __init__(self, file_path):
        self.file_path = file_path
        self.timestamp = datetime.now().timestamp()
        self.export_path = gettempdir() + f"/upload/{int(self.timestamp)}"
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
            logging.info(f"[FILE] Creating temp directory. Does {self.export_path} exist - {str(os.path.exists(self.export_path))}")
    
    def extractFile(self, zFile, password):
        zFile.setpassword(password)
        return zFile.try7z()

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
        logging.info(f"[7z] Cracking 7z with dict {dict_path}")
        # dict_path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'dict.txt')
        dname = self.fromDictionary(dict_path)
        try:
            zf = SevenZipFile(file_path=self.file_path)
            if not zf.need_password():
                self.clear_file(self.file_path)
                return 'EMPTY_PASSWORD'
            for line in dname:
                found = self.extractFile(zf, line)
                if found == True:
                    self.clear_file(self.file_path)
                    return line
            logging.info(f"[7z] Cracking 7z with with dict {dict_path} not succeded")
            self.clear_file()
            return None
        except FileNotFoundError:
            pass

    def brute_crack(self):
        logging.info(f"[7z] Cracking 7z with brute force")
        ALPHABET = "abcdefghijklmtnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=[]{}|\\:~<>?"
        min_pas_len = 1
        max_pas_len = 5
        try:
            for i in range(min_pas_len,max_pas_len+1):
                # ALPHABET = ''.join(random.sample(ALPHABET,len(ALPHABET))) # shuffle alphabet 
                listPass = product(ALPHABET, repeat=i)
                zf = SevenZipFile(file_path=self.file_path)
                try:
                    if not zf.need_password():
                        zf.close()
                        self.clear_file(self.file_path)
                        return 'EMPTY_PASSWORD'
                except RuntimeError as e:
                    pass
                for line in listPass:
                    line = ''.join(line)
                    # print(line)
                    found = self.extractFile(zf, line)
                    if found == True:
                        self.clear_file(self.file_path)
                        return line
            logging.info(f"[7z] Cracking 7z with brute force not succeded")
            self.clear_file()
            return None
        except FileNotFoundError:
            pass

class SevenZipFile():
    def __init__(self, file_path):
        self.file_path = file_path
        self.password = None

    def setpassword(self, password):
        self.password = password

    def need_password(self):
        cmd = ["7z", "t", self.file_path, "-p"]
        system = subprocess.run(cmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out, err = system.communicate()
        if system.stderr.decode() == "":
            return False
        else:
            return True
    
    def try7z(self):
        cmd = ["7z", "t", self.file_path, f"-p{self.password}"]
        system = subprocess.run(cmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if system.stderr.decode() == "":
            return True
        else:
            return False

def crack_zip(file_path):
    logging.info('[7z] Decrypting 7z file')
    dict_txt_files = glob.glob(rf"./logged_in/archive_cracker/dictionaries/*.txt") # Lista słówników z folderu
    if len(dict_txt_files) == 0:
        logging.error('[7z] Dict not found')
        exit(1)
    future_list = []
    with ProcessPool(max_workers=2, max_tasks=1000) as pool:
        #future_list.append(pool.schedule(SevenZip(file_path).brute_crack))
        for dict_path in dict_txt_files:
            future_list.append(pool.schedule(SevenZip(file_path).check_zip, args=(dict_path,)))
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
    # z = SevenZip("./test.7z")
    # ret = crack_zip("./test.7z")
    # ret = crack_zip("./test.zip")
    # print(ret)