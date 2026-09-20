import mailer
from os import getenv

def setup_client() -> mailer.MailClient:
    """
    Sets up the MailClient using environment variables.

    Returns:
        mailer.MailClient: An instance of the MailClient configured with environment variables.
    """

    # Retrieve email configuration from environment variables
    smtp_server = getenv("MAIL_SERVER")
    port = int(getenv("PORT"))
    sender_email = getenv("SENDER_EMAIL")
    sender_password = getenv("SENDER_PASSWORD")

    # Create and return a MailClient instance
    return mailer.MailClient(smtp_server, port, sender_email, sender_password)

def setup_client_manually(smtp_server: str, port: int, sender_email: str, sender_password: str) -> mailer.MailClient:
    return mailer.MailClient(smtp_server, port, sender_email, sender_password)