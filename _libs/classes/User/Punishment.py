class Punishment:
    def __init__(
            self,
            id : int,
            user_id : int,
            admin_id : int,
            reason : str,
            duration : int,
            issued_at : int
    ):
        self.id = id
        self.user_id = user_id
        self.admin_id = admin_id
        self.reason = reason
        self.duration = duration
        self.issued_at = issued_at
    def getID(self) -> int:
        return self.id
    def getUserID(self) -> int:
        return self.user_id
    def getAdminID(self) -> int:
        return self.admin_id
    def getReason(self) -> str:
        return self.reason
    def getDuration(self) -> int:
        return self.duration
    def getIssuedAt(self) -> int:
        return self.issued_at
    def setReason(self, reason : str) -> None:
        self.reason = reason
    def setDuration(self, duration : int) -> None:
        self.duration = duration
