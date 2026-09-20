import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient: str, subject: str, body: str, sender: str, password: str, smtp_server: str, port: int, live_server: smtplib.SMTP = None) -> bool:
    """
    Send a single plain-text email.

    Args:
        recipient: The recipient's email address.
        subject: The email subject.
        body: The plain-text message body.
        sender: The sender's email address.
        password: The sender's SMTP password.
        smtp_server: The SMTP server hostname.
        port: The SMTP server port.
        live_server: An existing connection, used when sending a batch.

    Returns:
        True if the message was sent successfully, otherwise False.
    """

    # build the MIME message shared by both sending paths.
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # reuse the caller's connection when sending as part of a batch.
    if live_server:
        try:
            live_server.sendmail(sender, recipient, msg.as_string())
            return True
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")
            return False

    # open and authenticate a connection for a standalone message.
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            if port == 587:
                server.starttls()

            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email sent successfully to {recipient}")
        return True
    
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")
        return False

def send_batch(recipients: list, subject: str, body: str, personalisation: dict, sender: str, password: str, smtp_server: str, port: int) -> None:
    """
    Send personalized plain-text emails over one SMTP connection.

    The personalization mapping is keyed by recipient. Values are substituted
    into the subject and body using ``str.format`` syntax, such as ``{name}``.

    Args:
        recipients: The recipient email addresses.
        subject: The email subject template.
        body: The plain-text body template.
        personalisation: Recipient-specific values for template substitution.
        sender: The sender's email address.
        password: The sender's SMTP password.
        smtp_server: The SMTP server hostname.
        port: The SMTP server port.

    Returns:
        The fraction of recipients whose messages were sent successfully.
    """

    success = 0
    total = len(recipients)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            if port == 587: # explicit TLS
                server.starttls()

            server.login(sender, password)

            for recipient in recipients:
                try:
                    # render templates with values specific to this recipient.
                    values = personalisation.get(recipient, {})
                    personalised_subject = subject.format(**values)
                    personalised_body = body.format(**values)

                    send_email(
                        recipient,
                        personalised_subject,
                        personalised_body,
                        sender,
                        password,
                        smtp_server,
                        port,
                        live_server=server,
                    )
                    success += 1

                except Exception as e:
                    print(f"Error sending email to {recipient}: {e}")

    except Exception as e:
        print(f"Error sending batch emails [No recipient received]: {e}")
        return 0 # no success

    return success/total # percentage of success