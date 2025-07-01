# 📁 utils/email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "metraa2004@gmail.com"  # 🔒 твоя почта
APP_PASSWORD = "lgpwwegfatoqujjl"  # 🔐 пароль приложения

def send_user_email(name: str, phone: str, to_email: str):
    subject = "Новый пользователь добавлен ✅"
    body = f"""
    👤 Имя: {name}
    📞 Телефон: {phone}
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)
