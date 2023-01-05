import smtplib
import ssl
import api_keys


port = 465
email_user = api_keys.email_username
password = api_keys.email_app_password

context = ssl.create_default_context()


def send_email(message):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_user, password)
        server.sendmail(email_user,email_user,message)

