import bcrypt

pwd = "Ivoves20$".encode()
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(pwd, salt)
print(hashed)