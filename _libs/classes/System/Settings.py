class Settings:
    def __init__(
            self,
            terms : str,
            contacts : str,
            auth_enabled : bool,
            service_mode : bool,
            mail_host : str,
            mail_port : int,
            mail_from : str,
            mail_user : str,
            mail_pass : str,
            panel_pass : str,
            password_salt : str,
            version : str            
    ):
        self.terms = terms
        self.contacts = contacts
        self.auth_enabled = auth_enabled
        self.service_mode = service_mode
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_from = mail_from
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.panel_pass = panel_pass
        self.password_salt = password_salt
        self.version = version
    def getTerms(self) -> str:
        return self.terms
    def getContacts(self) -> str:
        return self.contacts
    def isAuthEnabled(self) -> bool:
        return self.auth_enabled
    def isServiceMode(self) -> bool:
        return self.service_mode
    def getMailHost(self) -> str:
        return self.mail_host
    def getMailPort(self) -> int:
        return self.mail_port
    def getMailFrom(self) -> str:
        return self.mail_from
    def getMailUser(self) -> str:
        return self.mail_user
    def getMailPass(self) -> str:
        return self.mail_pass
    def getPanelPass(self) -> str:
        return self.panel_pass
    def getPasswordSalt(self) -> str:
        return self.password_salt
    def getVersion(self) -> str:
        return self.version