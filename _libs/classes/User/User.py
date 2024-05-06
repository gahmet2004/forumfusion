class User:
    def __init__(self) -> None:
        self.id = None
        self.tag = None
        self.email = None
        self.password = None
        self.group = None
        self.last_seen = None
        self.registration = None
        
    def upload(self):
        return
    def download(self):
        return
    def getId(self) -> int:
        return self.id
    def getTag(self) -> str:
        return self.tag
    def getEmail(self) -> str:
        return self.email
    def getLastSeen(self) -> int:
        return self.last_seen
    def getRegistration(self) -> int:
        return self.registration
    def setGroup(self, group : str) -> None:
        self.group = group
        return self.upload()
    def setLastSeen(self, last_seen : int) -> None:
        self.last_seen = last_seen
        return self.upload()
    def setTag(self, tag : int) -> None:
        self.tag = tag
        return self.upload()
    def setPassword(self, password : str) -> None:
        self.password = password
        return self.password


def getByID(id : int) -> User:
    """
    Return User by identificator;
    """

def getByTag(tag : str) -> User:
    """
    Return User by user tag;
    """