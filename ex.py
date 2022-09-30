
# import base64
from base64 import b64decode
from base64 import b64encode
  
s = b'Hello World'
s = b64encode(s)
print("encoded value:",s)
# Using base64.b64decode() method
gfg = b64decode(s)
  
print("decoded value:",gfg)