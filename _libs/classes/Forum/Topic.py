class Topic:
    def __init__(
            self,
            id : int,
            subcat_id : int,
            author : int,
            name : str,
            preview : str,
            content : str,
            subscribers : list,
            banned : bool,
            ban_meta : dict,
            last_edit : int,
            issued : int
    ):
        self.id = id
        self.subcat_id = subcat_id
        self.author = author
        self.name = name
        self.preview = preview
        self.content = content
        self.subscribers = subscribers
        self.banned = banned
        self.ban_meta = ban_meta
        self.last_edit = last_edit
        self.issued = issued
    def getID(self) -> int:
        return self.id
    def getSubcatID(self) -> int:
        return self.subcat_id
    def getAuthor(self) -> int:
        return self.author
    def getName(self) -> str:
        return self.name
    def getPreview(self) -> str:
        return self.preview
    def getContent(self) -> str:
        return self.content
    def getSubs(self) -> list:
        return self.subscribers
    def isBanned(self) -> bool:
        return self.ban_meta
    def getBanMeta(self) -> dict:
        return self.ban_meta
    def getLastEdit(self) -> int:
        return self.last_edit
    def getIssued(self) -> int:
        return self.issued
    def setSubcatID(self, id : int) -> None:
        self.subcat_id = id
    def setName(self, name : str) -> None:
        self.name = name
    def setPreview(self, preview : str) -> None:
        self.preview = preview
    def setContent(self, content : str) -> None:
        self.content = content
    def setSubs(self, subs : list) -> None:
        self.subscribers = subs
    def setBanned(self, ban : bool) -> None:
        self.banned = ban
    def setBanMeta(self, meta : dict) -> None:
        self.ban_meta = meta
    def setLastEdit(self, last_edit : int) -> None:
        self.last_edit = last_edit