import mailer
from os import getenv

def setup_client_from_env() -> mailer.MailClient:
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