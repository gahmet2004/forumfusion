from smtplib import SMTP as smtp

class MailService:
    def __init__(
            self,
            m_host : str,
            m_port : int,
            m_from : str,
            m_user : str,
            m_pass : str
    ):
        """
        host : localhost,
        port : 443,
        from : "mail@mail.mail",
        user : root,
        pass : root
        """
        self.host = m_host
        self.port = m_port
        self.user = m_user
        self.m_from = m_from
        self.m_pass = m_pass
    def send_message(
            self,
            subject : str,
            to : str,
            message : str
    ):
        server = smtp(self.host, self.port)
        server.login(
            self.user,
            self.m_pass
        )
        body = "\r\n".join((
            "From: %s" % self.m_from,
            "To: %s" % to,
            "Subject: %s" % subject,
            "",
            message
        ))
        server.sendmail(
            self.m_from,
            to,
            body
        )
        server.quit()

a = MailService(
    "smtp.timeweb.ru",
    2525,
    "forum@gallahad.ru",
    "forum@gallahad.ru",
    "Ivoves20$"
)
a.send_message(
    "HI MAAAAN! I am here to test SMTP lib.",
    "sobol.zh@phystech.edu",
    "Your Test Code is 111223123123123"
)