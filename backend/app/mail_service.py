import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class MailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "surajsutar8154@gmail.com"
        self.sender_password = "vukf caaa qvrr lttj"

    def send_reset_otp(self, receiver_email, otp):
        if not self.sender_email or not self.sender_password:
            print("SMPT Error: Missing credentials in .env")
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = "WoundSense AI - Password Reset OTP"
        message["From"] = f"WoundSense AI Support <{self.sender_email}>"
        message["To"] = receiver_email

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                <h2 style="color: #0F52BA;">WoundSense AI Platinum</h2>
                <p>Hello Doctor,</p>
                <p>You requested a password reset for your Surgical Intelligence console.</p>
                <div style="background: #f4f7fe; padding: 15px; text-align: center; border-radius: 8px; margin: 20px 0;">
                    <span style="font-size: 24px; font-weight: bold; letter-spacing: 5px; color: #0F52BA;">{otp}</span>
                </div>
                <p>This OTP will expire in 10 minutes. If you did not request this, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin-top: 20px;">
                <p style="font-size: 11px; color: #999; text-align: center;">Clinical Security Powered by WoundSense Intelligence Node</p>
            </div>
        </body>
        </html>
        """
        part = MIMEText(html, "html")
        message.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
            return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False

mail_service = MailService()
