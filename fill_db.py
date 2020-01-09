import requests
from time import sleep
data = {
    'uname':'root',
    'pwd':'root'
}

modes = [
    'md5',
    'sha256',
    'sha1',
    'sha384',
    'sha512'
]
i = 0
imax = 3330
url = 'https://arqsz.net'
try:
    with requests.Session() as s:
        response = s.post(url + '/out/signin', data=data)
        print(response)
        with open('dict_PL.txt', 'r') as f:
            for line in f:
                i += 1
                if imax > i:
                    continue
                words = line.strip().split(', ')
                for word in words:
                    for mode in modes:
                        payload = {
                            'text_to_encode':word,
                            'mode':mode
                        }
                        response = s.post(url + '/in/hash/encode', data=payload)
except KeyboardInterrupt:
    print(i)
