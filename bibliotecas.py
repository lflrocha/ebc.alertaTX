import smtplib, ssl
from os.path import dirname, abspath
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def enviaEmail(assunto, mensagem, destinatarios):
    msg = MIMEMultipart()
    msg['From'] = "automacoes@ebc.com.br"
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem))
    smtp = smtplib.SMTP("smtp.ebc.com.br", 587)
    smtp.starttls()
    smtp.login('automacoes', '84oXHKsvgu')
    smtp.sendmail(msg['From'], destinatarios, msg.as_string())
    smtp.quit()
