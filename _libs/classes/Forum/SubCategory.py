class SubCategory:
    def __init__(
            self,
            id : int,
            cat_id : int,
            name : str,
            descript : str,
            subscribers : list,
            moderators : list,
            creator_id : int,
            issued : int
    ):
        self.id = id
        self.cat_id = cat_id
        self.name = name
        self.descript = descript
        self.subscribers = subscribers
        self.moderators = moderators
        self.creator_id = creator_id
        self.issued = issued
    def getID(self) -> int:
        return self.id
    def getCatID(self) -> int:
        return self.cat_id
    def getName(self) -> str:
        return self.name
    def getDescript(self) -> str:
        return self.descript
    def getSubs(self) -> list:
        return self.subscribers
    def getMods(self) -> list:
        return self.moderators
    def getCreator(self) -> int:
        return self.creator_id
    def getIssued(self) -> int:
        return self.issued
    def setCatID(self, id : int) -> None:
        self.cat_id = id
    def setName(self, name : str) -> None:
        self.name = name
    def setDescript(self, descript : str) -> None:
        self.descript = descript
    def setSubs(self, subs : list) -> None:
        self.subscribers = subs
    def setMods(self, mods : list) -> None:
        self.moderators = mods