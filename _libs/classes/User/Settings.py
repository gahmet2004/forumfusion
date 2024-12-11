class Settings:
    def __init__(
            self, 
            id : int,
            email_new_topic_event : bool,
            email_new_review_event : bool,
            email_follower_event : bool,
            email_broadcast : bool,
            hide_email : bool
    ):
        self.id = id
        self.email_new_topic_event = email_new_topic_event
        self.email_new_review_event = email_new_review_event
        self.email_follower_event = email_follower_event
        self.email_broadcast = email_broadcast
        self.hide_email = hide_email
    def getID(self) -> int:
        return self.id
    def isEmailNewTopicEvent(self) -> bool:
        return self.email_new_topic_event
    def isEmailNewReviewEvent(self) -> bool:
        return self.email_new_review_event
    def isEmailFollowerEvent(self) -> bool:
        return self.email_follower_event
    def isEmailBroadcast(self) -> bool:
        return self.email_broadcast
    def isHideEmail(self) -> bool:
        return self.hide_email
    def setEmailNewTopicEvent(self, value : bool) -> None:
        self.email_new_topic_event = value
    def setEmailNewReviewEvent(self, value : bool) -> None:
        self.email_new_review_event = value
    def setEmailFollowerEvent(self, value : bool) -> None:
        self.email_follower_event = value
    def setEmailBroadcast(self, value : bool) -> None:
        self.email_broadcast = value
    def setHideEmail(self, value : bool) -> None:
        self.hide_email = value
