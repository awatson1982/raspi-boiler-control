import password2
from passlib.hash import sha512_crypt


password = 'tuppence'
hashedPassword = '$6$rounds=656000$BkpowmQxtA..Hfv5$7okz..MlBuyYIsH7JwsJOzFZDsuTLLTZKDY5HCmqt5n3lSRzZiuVOEQW0OAAW71XA53BgUgKKINnojbc./dM11'

if sha512_crypt.verify(password, hashedPassword):
    print("password correct")
