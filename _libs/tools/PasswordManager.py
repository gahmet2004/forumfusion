import bcrypt

def hash(password : str):
    """
    Hashing the password with salt;
    """
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(
        password.encode('utf-8'),
        salt
    )
    return hash
def isValid(password, hash : str):
    """
    Comparing 
    """