import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class MailService:
    def __init__(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.app_password =os.getenv("APP_PASSWORD") # Mot de passe d'application généré pour votre compte Gmail

    def sendEmail(self,to_email,file_link):
        print("test service")
        # Connexion au serveur SMTP de Gmail
        self.server.login(self.sender_email, self.app_password)
         
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = to_email
        message['Subject'] = "gros chibrax"
        
        message.attach(MIMEText("voici " + file_link ,'plain'))
        
           # Envoi du message
        self.server.sendmail(self.sender_email, to_email, message.as_string())

    # Déconnexion du serveur SMTP
        self.server.quit()

        print("Email envoyé avec succès !")