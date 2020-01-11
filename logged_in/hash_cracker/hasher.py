#!/usr/bin/env python3

import re
import os
import requests
import argparse
import concurrent.futures
from database.models import Hash, db
cwd = os.getcwd()


def alpha(hashvalue, hashtype):
    return False

def beta(hashvalue, hashtype):
    response = requests.get('https://hashtoolkit.com/reverse-hash/?hash=' + hashvalue, verify=False).text
    match = re.search(r'/generate-hash/?text=.*?"', response)
    if match:
        return match.group(1)
    else:
        return False

def gamma(hashvalue, hashtype):
    response = requests.get('https://www.nitrxgen.net/md5db/' + hashvalue, verify=False).text
    if response:
        return response
    else:
        return False

def delta(hashvalue, hashtype):
    data = f"__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=lkbQ0EkLkhbyS5cKCHuEF172jcrOmSxyXx1HrJ6rsrseyaAX0thLqXT7sawHhNu2ZxFb2T8JbhJn0wX1Jglq6%2F3efhuywRDTlNmlP5wzDslmwYBvVrxjTdy9B3PYJORftvNrGnmPyVgaspARyWPPVAEfZWuHAjPNDo0phNG%2FpChlLztesUDWIP0P%2FCbINFoSpirAngSnIVxIH7lKzhGZIkvAMmuV009BoYV3LzuLOW7iRC9XUouY8DRXKB58PoRqv9sYfD3n%2Fy82Wh6%2Fh8oBO8c78MKVHopegWw5m5i6WQuyODKifY%2BqSnps8bV2ehe9VYbScsdkwqm6khMXh205aBYauAvQKf5u3ZKG8edfC4egBRl%2BYGxNhzyiXXJbxQQvQ%2B%2FERJuxf2ALHT6T%2BccvYlKJcgSdeVZiZ4B3uLlC3Oz8v5%2FqacUA5IvvLG7fmhofMGGGKBs%2BncTVeMPaJ%2FAiw60IwBoCxy3iiU8Vi3KxJZOnZzJaliZz1QlmXt09ILcRVQYRVbx9lSRb1C2akfSQBaRgEdQvtjs%2F%2Bcl59pY0D49CEnYZNS0iTDe4CXfPWOh5XDJGKHhCFDdxvnbUvEAyAGTL80D8V4IPuPN2ORhrmqur9NIzVDrwfwFDRwP21r29nGhq%2BtWD4pXcadKm%2FVjLdmR67zpBYgr1jsaujLJzJ4kcEPtbIRrB7QjXMPlZFw%2F5p62ryTfIc5z%2BlAluVBSr9gkIfnI7uZ%2FYczskttXi3JfxBG269glYHtgCzUz1YmighypIaqQ56aBJe9G9CCy%2F20ho%2FaKkAN0ia2cTER47oWEaWaeE5hF7L1%2B8iTIqIv3uMR2RENwBCJb6vCFJyFLfuPnNWBNrG3FpZN1ZXtD5xKeV3kTEG1yEQmORWm6q3CJSArZukxBh8EeRu8bZ5d90CtrKpbiwnH9oplAEq00ARrPkvJh7%2BztZSisqRYii0fy7D7spc7zwCg2Lz7G0xYCreifur9EgUnS71LsXMD0x%2FR23VpFmic55Pla8YQhjGrMMi%2F8rGUh15fasAEydGI7WK7PitQo1xqp3P5SqTPddbV4wF6SgIjGdu0YXTiGOJHsFx3AZx1GNnuHDDkalW%2FfbmncC5OIspbY0psFyxoiNsmTZ0Et%2FURYKkuu5P6qcrCupYqdcSLFlXy8b%2BR9xE8DY9iZxF%2B88%2Fc52Vd6R1uHuJmSTGQDfx431VnNK%2Byr6fCcfY2QNZ05tXlr%2F%2FLyusqrnoY2Oiay5KxnhWyuvjqxljjTgJahl2eNKaMwQcQ6i%2B14kNWkfBwgcIX62MT2TilYEhoZnNOQ%3D&__VIEWSTATEGENERATOR=CA0B0334&ctl00%24ContentPlaceHolder1%24TextBoxInput={hashvalue}&ctl00%24ContentPlaceHolder1%24InputHashType={hashtype}&ctl00%24ContentPlaceHolder1%24Button1=decrypt&ctl00%24ContentPlaceHolder1%24HiddenFieldAliCode=&ctl00%24ContentPlaceHolder1%24HiddenField1=&ctl00%24ContentPlaceHolder1%24HiddenField2=g75vZOyWxV9hVomPlT6%2FR34Stz60p4OHgvbuosn%2BxCZZ304jdeuNwA%3D%3D"
    header = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Origin": "https://www.cmd5.org"
    }
    response = requests.post('https://www.cmd5.org/', headers=header, data=data, verify=False).text
    match = re.search(r'<span id="LabelAnswer" class="LabelAnswer" onmouseover="toggle();">(.*?)</span>', response)
    if match:
        if "payment record" in match.group(1) or "failed" in match.group(1):
            return False
        return match.group(1)
    else:
        return False

def theta(hashvalue, hashtype):
    response = requests.get('https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728' % (hashvalue, hashtype), verify=False).text
    if len(response) != 0:
        return response
    else:
        return False

md5 = [gamma, alpha, beta, theta, delta]
sha1 = [alpha, beta, theta, delta]
sha256 = [alpha, beta, theta, delta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta, delta]

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
        result[hashvalue] = resp

def single(args):
    result = crack(args.hash, args.hash_type)
    if result:
        print (result)
    else:
        return

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
            h = Hash(hash_type, hash, result)
            db.session.add(h)
            try:
                db.session.commit()
            except Exception as e:
                pass
            return (result)
        else:
            return False
    else:
        return try_db
