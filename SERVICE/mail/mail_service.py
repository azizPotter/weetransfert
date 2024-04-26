import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from SERVICE.crypto.crypto_service import CryptoService

crypto_service = CryptoService()

class MailService:
    def __init__(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.app_password =os.getenv("APP_PASSWORD") # Mot de passe d'application généré pour votre compte Gmail

    def sendEmail(self,to_email,file_link):
        # Connecting to Gmail SMTP server
        self.server.login(self.sender_email, self.app_password)
         
        to_email_crypted = crypto_service.hash_data(to_email)
        from_email_crypted = crypto_service.hash_data(self.sender_email)
        print("fileLink " + file_link)
        url = "http://127.0.0.1:8080/download_view?file_path=" + crypto_service.encrypt_url(file_link, from_email_crypted, to_email_crypted) + "&to=" + to_email_crypted + "&from=" + from_email_crypted

        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = to_email
        message['Subject'] = "File sharing"

        message.attach(MIMEText("You can recover your file via this link :\n " + url ,'plain'))
        
        # Sending the message
        self.server.sendmail(self.sender_email, to_email, message.as_string())

    # Déconnexion du serveur SMTP
        self.server.quit()

        print("Email sent successfully!")