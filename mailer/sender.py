import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient: str, subject: str, body: str, sender: str, password: str, smtp_server: str, port: int, live_server: smtplib.SMTP = None) -> bool:
    """
    Sends a single email to the specified recipient.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body content of the email.
        sender (str): The sender's email address.
        password (str): The sender's email password.
        smtp_server (str): The SMTP server address.
        port (int): The port number for the SMTP server.
        live_server (smtplib.SMTP, optional): An existing SMTP server connection used for batching. Defaults to none.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """

    # construct the payload
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # if a server is supplied, send it via that (for batching)
    if live_server:
        try:
            live_server.sendmail(sender, recipient, msg.as_string())
            return True
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")
            return False

    # otherwise, create a new connection and send the email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            if port == 587: # explicit TLS
                server.starttls()

            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")
        return False