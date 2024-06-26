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

def dict_to_Settings(data : dict) -> Settings:
    return Settings(
        data['terms'],
        data['contacts'],
        data['auth_enabled'],
        data['service_mode'],
        data['mail_host'],
        data['mail_port'],
        data['mail_from'],
        data['mail_user'],
        data['mail_pass'],
        data['panel_pass'],
        data['password_salt'],
        data['version']
    )
def settings_to_dict(data : Settings) -> dict:
    response = {
        "terms" : data.getTerms(),
        "contacts" : data.getContacts(),
        "auth_enabled" : data.isAuthEnabled(),
        "service_mode" : data.isServiceMode(),
        "mail_host" : data.getMailHost(),
        "mail_port" : data.getMailPort(),
        "mail_from" : data.getMailFrom(),
        "mail_user" : data.getMailUser(),
        "mail_pass" : data.getMailPass(),
        "panel_pass" : data.getPanelPass(),
        "password_salt" : data.getPasswordSalt(),
        "version" : data.getVersion()
    }
    return response