import mailer
import dotenv

def setup_client() -> mailer.MailClient:
    """
    Sets up the MailClient using environment variables.

    Returns:
        mailer.MailClient: An instance of the MailClient configured with environment variables.
    """
    # Load environment variables from .env file
    dotenv.load_dotenv()
    dotenv_path = dotenv.find_dotenv()

    # Retrieve email configuration from environment variables
    smtp_server = dotenv.get_key(dotenv_path, "MAIL_SERVER")
    port = int(dotenv.get_key(dotenv_path, "PORT"))
    sender_email = dotenv.get_key(dotenv_path, "SENDER_EMAIL")
    sender_password = dotenv.get_key(dotenv_path, "SENDER_PASSWORD")

    # Create and return a MailClient instance
    return mailer.MailClient(smtp_server, port, sender_email, sender_password)