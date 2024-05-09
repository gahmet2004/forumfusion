class User:
    def __init__(
            self,
            id : int = None,
            tag : str = None,
            email :str = None,
            password :str = None,
            group :str = None,
            last_seen :int = None,
            registration : int = None
    ):
        """
        get instance of User object.
        """
        self.id = id
        self.tag = tag
        self.email = email
        self.password = password
        self.group = group
        self.last_seen = last_seen
        self.registration = registration
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
    def setLastSeen(self, last_seen : int) -> None:
        self.last_seen = last_seen
    def setTag(self, tag : int) -> None:
        self.tag = tag
    def setPassword(self, password : str) -> None:
        self.password = password