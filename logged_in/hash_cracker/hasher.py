#!/usr/bin/env python3

import re
import os
import requests
import argparse
import concurrent.futures
from database.models import Hash
cwd = os.getcwd()


def alpha(hashvalue, hashtype):
    return False

def beta(hashvalue, hashtype):
    response = requests.get('https://hashtoolkit.com/reverse-hash/?hash=' + hashvalue).text
    match = re.search(r'/generate-hash/?text=.*?"', response)
    if match:
        return match.group(1)
    else:
        return False

def gamma(hashvalue, hashtype):
    response = requests.get('https://www.nitrxgen.net/md5db/' + hashvalue).text
    if response:
        return response
    else:
        return False

def delta(hashvalue, hashtype):
    #data = {'auth':'8272hgt', 'hash':hashvalue, 'string':'','Submit':'Submit'}
    #response = requests.post('http://hashcrack.com/index.php' , data).text
    #match = re.search(r'<span class=hervorheb2>(.*?)</span></div></TD>', response)
    #if match:
    #    return match.group(1)
    #else:
    return False

def theta(hashvalue, hashtype):
    response = requests.get('https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728' % (hashvalue, hashtype)).text
    if len(response) != 0:
        return response
    else:
        return False

md5 = [gamma, alpha, beta, theta, delta]
sha1 = [alpha, beta, theta, delta]
sha256 = [alpha, beta, theta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta]

def crack(hashvalue, hash_type):
    result = False
    if hash_type == 'md5':
        for api in md5:
            r = api(hashvalue, 'md5')
            if r:
                return r
    elif hash_type == 'sha1': #len(hashvalue) == 40:
        for api in sha1:
            r = api(hashvalue, 'sha1')
            if r:
                return r
    elif hash_type == 'sha256': #len(hashvalue) == 64:
        for api in sha256:
            r = api(hashvalue, 'sha256')
            if r:
                return r
    elif hash_type == 'sha384': #len(hashvalue) == 96:
        for api in sha384:
            r = api(hashvalue, 'sha384')
            if r:
                return r
    elif hash_type == 'sha512': #len(hashvalue) == 128:
        for api in sha512:
            r = api(hashvalue, 'sha512')
            if r:
                return r
    else:
        return False

result = {}

def threaded(hashvalue):
    resp = crack(hashvalue)
    if resp:
        print (hashvalue + ' : ' + resp)
        result[hashvalue] = resp

def single(args):
    result = crack(args.hash, args.hash_type)
    if result:
        print (result)
    else:
        print ('%s Hash was not found in any database.' % bad)

def get_from_db(hash, hash_type):
    h = Hash.query.filter_by(hash_type=hash_type).filter_by(hashed_text=hash).first()
    if h is None:
        return None
    else:
        return h.plain_text

def single(hash, hash_type):
    try_db = get_from_db(hash, hash_type)
    if try_db is None:
        result = crack(hash, hash_type)
        if result:
            return (result)
        else:
            return False
    else:
        return try_db
