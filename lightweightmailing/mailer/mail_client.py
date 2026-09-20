from .sender import send_email, send_batch

class MailClient():
    """
    A simple SMTP client to send emails. This is a simple wrapper around the send_email and send_batch functions.
    """

    def __init__(self, smtp_server: str, port: int, sender_email: str, sender_password: str):
        """
        Configure a simple smpt client to send emails. This is a simple wrapper around the send_email and send_batch functions.
        """

        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password

    # wrappers of sender.send_email and send_batch.

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Sends a single email to the specified recipient.

        Args:
            recipient (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body content of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        return send_email(
            recipient,
            subject,
            body,
            self.sender_email,
            self.sender_password,
            self.smtp_server,
            self.port
        )

    def send_batch(self, recipients: list, subject: str, body: str, personalisation: dict) -> None:
        """
        Sends a batch of emails to the specified recipients. Text may contain personalisation via the personalisation dictionary. Structure:

        dict = {
            recipient : {
                "personalisation_key": "personalisation_value"
            }
        }

        Args:
            recipients (list): A list of email addresses to send the email to.
            subject (str): The subject of the email.
            body (str): The body content of the email.
            personalisation (dict): A dictionary containing personalisation data for each recipient.

        Returns:
            Percentage of successful sends. 
        """

        return send_batch(
            recipients,
            subject,
            body,
            personalisation,
            self.sender_email,
            self.sender_password,
            self.smtp_server,
            self.port
        )