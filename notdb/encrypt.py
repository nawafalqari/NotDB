from pyonr import loads
import base64 as b

def encode(data):
   '''
   encode data using `base64`
   '''
   return b.b64encode(str(data).encode('utf-8')) if not isinstance(data, bytes) else b.b64encode(data)

def decode(data):
   '''
   decode `base64` bytes
   '''
   return b.b64decode(str(data).encode('utf-8')) if not isinstance(data, bytes) else b.b64decode(data)

def handleEncoded(encoded:bytes):
   return loads(decode(encoded).decode('utf-8'))