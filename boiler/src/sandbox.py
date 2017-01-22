import password2
from passlib.hash import sha512_crypt
import requests

# password = 'tuppence'
# hashedPassword = '$6$rounds=656000$BkpowmQxtA..Hfv5$7okz..MlBuyYIsH7JwsJOzFZDsuTLLTZKDY5HCmqt5n3lSRzZiuVOEQW0OAAW71XA53BgUgKKINnojbc./dM11'
# 
# if sha512_crypt.verify(password, hashedPassword):
#     print("password correct")


tempAPI = requests.get('http://192.168.0.52:8000/temp')
if tempAPI.status_code != 200:
    raise Exception('GET /temp/ {}'.format(tempAPI.status_code) )
print(tempAPI.json()['temp']) 