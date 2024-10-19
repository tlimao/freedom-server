from freedomserver.configuration.smtp_config import SmtpConfig

class MailSender:

    def __init__(self, smtp_config: SmtpConfig):
        self._smtp_config: SmtpConfig = smtp_config

    def send_email(self, message: str, to: str, sender: str, sender_name: str, subject: str) -> bool:
        print(f"{subject}\n\n{sender} {sender_name}\n{to}\n{message}")
        
        return True