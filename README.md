# Automated Mailing

A lightweight SMTP email client for sending individual and personalized batch emails.

## Setup

Add this repository to your existing Python project, then create a `.env` file using `.env.example` as a template:

```env
SENDER_EMAIL=youremail@example.com
SENDER_PASSWORD=yourpassword
MAIL_SERVER=smtp.example.com
PORT=587
```

Initialize the client with:

```python
import AutomatedMailing

client = AutomatedMailing.setup_client()
```

`setup_client()` loads the SMTP settings from `.env` and returns a configured `MailClient` instance.

## Usage

### Send an email

```python
success = client.send_email(
    "recipient@example.com",
    "Welcome",
    "Thanks for signing up.",
)

print(success)
```

`send_email()` accepts:

| Argument | Type | Description |
| --- | --- | --- |
| `recipient` | `str` | Recipient email address |
| `subject` | `str` | Email subject |
| `body` | `str` | Plain-text email body |

It returns `True` when the message is sent successfully and `False` otherwise.

### Send personalized batch emails

```python
recipients = [
    "ada@example.com",
    "grace@example.com",
]

subject = "Welcome, {name}!"
body = "Hi {name},\n\nThanks for joining us."

personalisation = {
    "ada@example.com": {
        "name": "Ada",
    },
    "grace@example.com": {
        "name": "Grace",
    },
}

success_rate = client.send_batch(
    recipients,
    subject,
    body,
    personalisation,
)
```

Placeholders use Python `str.format()` syntax. Each recipient receives a message rendered with their own personalization values.

`send_batch()` accepts:

| Argument | Type | Description |
| --- | --- | --- |
| `recipients` | `list[str]` | Recipient email addresses |
| `subject` | `str` | Subject template |
| `body` | `str` | Plain-text body template |
| `personalisation` | `dict` | Recipient-specific replacement values |

The function returns the fraction of messages sent successfully.