# LightweightMailing

LightweightMailing is a small, beginner-friendly SMTP wrapper for sending plain-text email from Python. It provides a simple client for sending one message or a batch of personalized messages over SMTP.

The package has no third-party runtime dependencies and supports Python 3.8 and later.

## Features

- Send a single plain-text email.
- Send personalized messages to multiple recipients over one SMTP connection.
- Use either environment variables or explicit configuration values.
- Use familiar Python `str.format` placeholders in batch subjects and bodies.
- Install directly from PyPI or use the source from GitHub.

## Installation

Install the latest published version from PyPI:

```bash
python -m pip install lightweightmailing
```

For a local checkout:

```bash
git clone https://github.com/prestondj/LightweightMailing.git
cd LightweightMailing
python -m pip install .
```

## Quick start

Create a client with your SMTP server details and send a message:

```python
from lightweightmailing import setup_client_manually

client = setup_client_manually(
	smtp_server="smtp.example.com",
	port=587,
	sender_email="you@example.com",
	sender_password="your-smtp-password",
)

sent = client.send_email(
	recipient="recipient@example.com",
	subject="Hello from Python",
	body="This is a plain-text email sent with LightweightMailing.",
)

if sent:
	print("Email sent")
```

`send_email` returns `True` when the message is submitted successfully and `False` when the send fails. Errors are printed by the package.

## Environment-based configuration

`setup_client()` reads these values from the process environment:

| Variable | Description |
| --- | --- |
| `LIGHTWEIGHT_MAILER_MAIL_SERVER` | SMTP server hostname, such as `smtp.example.com` |
| `LIGHTWEIGHT_MAILER_PORT` | SMTP port as an integer. 587 for explicit TLS, or 465 for implicit TLS (587 is reccommended).
| `LIGHTWEIGHT_MAILER_SENDER_EMAIL` | Authenticated sender email address |
| `LIGHTWEIGHT_MAILER_SENDER_PASSWORD` | SMTP password or provider-issued app password |

Set the variables before starting Python:

```bash
export LIGHTWEIGHT_MAILER_MAIL_SERVER="smtp.example.com"
export LIGHTWEIGHT_MAILER_PORT="587"
export LIGHTWEIGHT_MAILER_SENDER_EMAIL="you@example.com"
export LIGHTWEIGHT_MAILER_SENDER_PASSWORD="your-smtp-password"
```

Then create the client:

```python
from lightweightmailing import setup_client

client = setup_client()
client.send_email(
	"recipient@example.com",
	"Environment-based configuration",
	"This message uses SMTP settings from the environment.",
)
```

The repository includes `.env.example` as a naming reference. LightweightMailing does not load `.env` files automatically; use a separate environment loader if you keep configuration in one.

## Personalized batch email

Use `{placeholder}` fields in the subject and body. The `personalisation` mapping is keyed by recipient address:

```python
from lightweightmailing import setup_client_manually

client = setup_client_manually(
	"smtp.example.com",
	587,
	"you@example.com",
	"your-smtp-password",
)

recipients = ["ada@example.com", "grace@example.com"]
personalisation = {
	"ada@example.com": {"name": "Ada"},
	"grace@example.com": {"name": "Grace"},
}

success_fraction = client.send_batch(
	recipients=recipients,
	subject="Hello, {name}",
	body="Hello {name},\n\nThanks for trying LightweightMailing.",
	personalisation=personalisation,
)

print(f"Sent {success_fraction:.0%} of messages")
```

`send_batch` returns a fraction between `0.0` and `1.0`, where `1.0` means every recipient was sent a message. A recipient without matching personalization values uses an empty mapping, so templates that require missing fields will fail for that recipient. An empty recipient list is not a useful input and should be avoided.

## SMTP and security notes

- Port `587` uses explicit TLS via `STARTTLS` before authentication.
- Other ports are opened with Python's regular `smtplib.SMTP` connection. Configure your SMTP provider accordingly; implicit TLS on port `465` is not enabled by this package.
- Use an app password or SMTP-specific credential when your provider supports it. Do not commit passwords, tokens, or populated `.env` files.
- This package sends plain-text email only. It does not provide HTML templates, attachments, retries, scheduling, delivery tracking, or unsubscribe management.
- Follow your provider's sending limits and applicable email and privacy laws.

## Public API

The package exports:

```python
from lightweightmailing import MailClient, setup_client, setup_client_manually
```

- `MailClient(smtp_server, port, sender_email, sender_password)` creates a configured client.
- `setup_client()` creates a client from the environment variables listed above.
- `setup_client_manually(...)` creates a client from explicit values.
- `MailClient.send_email(recipient, subject, body)` sends one plain-text message.
- `MailClient.send_batch(recipients, subject, body, personalisation)` sends personalized messages.

## Development

The project uses the standard `pyproject.toml` build configuration. To build distribution artifacts locally:

```bash
python -m pip install --upgrade build
python -m build
```

The published package is built and uploaded to PyPI when a GitHub release is published.

## License

LightweightMailing is released under the [MIT License](LICENSE).

Project homepage: [github.com/prestondj/LightweightMailing](https://github.com/prestondj/LightweightMailing)
