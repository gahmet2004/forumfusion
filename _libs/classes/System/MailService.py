from smtplib import SMTP as smtp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    def sendMessage(
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
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.m_from
        msg["To"] = to
        msg.attach(MIMEText(message))
        server.sendmail(
            self.m_from,
            to,
            msg.as_string()
        )
        server.quit()