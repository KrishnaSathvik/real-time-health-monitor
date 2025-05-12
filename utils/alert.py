import requests

def send_slack_alert(message):
    webhook_url = "https://hooks.slack.com/services/XXXX"
    payload = {"text": message}
    requests.post(webhook_url, json=payload)

def send_email_alert(subject, body, to_email):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("your_email@gmail.com", "your_app_password")
        smtp.send_message(msg)
