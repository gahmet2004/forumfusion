import bcrypt

pwd = "BabayKA222$$$".encode()
salt = bcrypt.gensalt()
pwd2 = "BabayKA222$$$".encode()
hashed = bcrypt.hashpw(pwd, salt)
hashed2 = bcrypt.hashpw(pwd2, salt)
print(hashed)
print(hashed2)