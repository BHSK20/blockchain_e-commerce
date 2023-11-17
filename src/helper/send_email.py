import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email details

def send_email(receiver_email, subject, message):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "bsh.ecommerce.noreply@gmail.com"
    sender_password = "jslwcmzbjhwpnwvf"
    # sender_password = "daylaweb123."

    # Create a multipart message and set the headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    try:
        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))
        # Create a SMTP object
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        # Start the TLS encryption
        smtp_obj.starttls()
        # Login to the SMTP server
        smtp_obj.login(sender_email, sender_password)
        # Send the email
        smtp_obj.sendmail(sender_email, receiver_email, msg.as_string())
        # Close the SMTP connection
        smtp_obj.quit()
    except NameError as e:
        print(e)