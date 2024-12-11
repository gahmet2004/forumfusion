class Profile:
    def __init__(
            self,
            id : int,
            name : str,
            avatar : str,
            about : str,
            subs : list,
            followers : list
    ):
        self.id = id
        self.name = name
        self.avatar = avatar
        self.about = about
        self.subs = subs
        self.followers = followers
    def getID(self) -> int:
        return self.id
    def getName(self) -> str:
        return self.name
    def getAvatar(self) -> str:
        return self.avatar
    def getAbout(self) -> str:
        return self.about
    def getSubs(self) -> list:
        return self.subs
    def getFollowers(self) -> list:
        return self.followers
    def setName(self, name : str) -> None:
        self.name = name
    def setAvatar(self, avatar : str) -> None:
        self.avatar = avatar
    def setAbout(self, about : str) -> None:
        self.about = about
    def setSubs(self, subs : list) -> None:
        self.subs = subs
    def setFollowers(self, followers : list) -> None:
        self.followers = followers