import bcrypt

_ENCODING = "utf-8"

def hashPassword(
        pswd : str,
        salt : str
) -> str:
    return bcrypt.hashpw(
        pswd.encode(encoding=_ENCODING),
        salt.encode(encoding=_ENCODING)
    ).decode(encoding=_ENCODING)

def getSalt() -> str:
    return bcrypt.gensalt().decode(encoding=_ENCODING)

def isValid(
        pswd : str,
        salt : str,
        hash : str
) -> bool:
    hashed = hashPassword(pswd, salt)
    return (hash.__eq__(hashed))