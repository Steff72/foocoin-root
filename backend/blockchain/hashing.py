import hashlib
import json

def hashing(*args):
    data = ''.join(sorted(map(lambda param: json.dumps(param), args)))

    return hashlib.sha256(data.encode('utf-8')).hexdigest()