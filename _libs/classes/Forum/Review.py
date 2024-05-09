class Review:
    def __init__(
            self,
            id : int,
            topic_id : int,
            author : int,
            content : str,
            banned : bool,
            ban_meta : dict,
            reaction : str,
            last_edit : int,
            issued : int
    ):
        self.id = id
        self.topic_id = topic_id
        self.author = author
        self.content = content
        self.banned = banned
        self.ban_meta = ban_meta
        self.reaction = reaction
        self.last_edit = last_edit
        self.issued = issued
    def getID(self) -> int:
        return self.id
    def getTopicID(self) -> int:
        return self.topic_id
    def getAuthor(self) -> int:
        return self.author
    def isBanned(self) -> bool:
        return self.banned
    def getBanMeta(self) -> dict:
        return self.ban_meta
    def getReaction(self) -> str:
        return self.reaction
    def getLastEdit(self) -> int:
        return self.last_edit
    def getIssued(self) -> int:
        return self.issued
    def setTopicID(self, id : int) -> None:
        self.topic_id = id
    def setBanned(self, banned : bool) -> None:
        self.banned = banned
    def setBanMeta(self, meta : dict) -> None:
        self.ban_meta = meta
    def setReaction(self, reaction : str) -> None:
        self.reaction = reaction
    def setLastEdit(self, last_edit : int) -> None:
        self.last_edit = last_edit