import jwt
import time

secreto = "123456"
ts = int(time.time())


token = jwt.encode({
    "id":"1","nombre": "Charles Roots","time": ts},
    secreto,
    algorithm='HS256'
    )
print('\n')
print('********** SHOWING JWT **********')
print(token)
print('********** SHOWING JWT **********')
print('\n')

resuelto = jwt.decode(token, secreto, algorithms=['HS256'])

print('********** SHOWING JWT DECODED ***********')
print(resuelto)
print('********** SHOWING JWT DECODED ***********')