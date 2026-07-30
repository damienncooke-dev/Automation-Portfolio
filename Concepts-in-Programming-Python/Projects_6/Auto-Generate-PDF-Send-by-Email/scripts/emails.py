#!/usr/bin/env python3


import email.message
import mimetypes
import os
import smtplib


def generate(sender, recipient, subject, body, attachment_path):
  """Creates an email with an attachement."""

  # Basic Email formatting
  message = email.message.EmailMessage()
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = subject
  message.set_content(body)

  # Process the attachment and add it to the email
  attachment_filename = os.path.basename(attachment_path)
  mime_type, _ = mimetypes.guess_type(attachment_path)
  mime_type, mime_subtype = mime_type.split('/', 1)

  with open(attachment_path, 'rb') as ap:
    message.add_attachment(ap.read(),
                          maintype=mime_type,
                          subtype=mime_subtype,
                          filename=attachment_filename)
  print(message)

  return message

def send(message, sender):
  """Sends the message to the configured SMTP server."""

  # Provide credentials for sending email (from sender to recipient)
  password = os.getenv("ICLOUD_APP_PASSWORD")
  with smtplib.SMTP("smtp.mail.me.com", 587) as mail_server:  # create an SMTP object with host and port
    mail_server.starttls()  # iCloud requires TLS on 587
    mail_server.login(sender, password)  # provide credentials
    mail_server.send_message(message)  # command to send email via SMTP
    print("Email sent successfully!")
    mail_server.quit()  # close connection to mailserver
