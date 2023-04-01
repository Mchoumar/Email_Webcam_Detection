import imghdr
import smtplib as st
from os import getenv
from email.message import EmailMessage


def send_email(image):
    # setup for the port and host
    host = "smtp.gmail.com"
    port = 587

    # setup for the username, password, and the receiver
    username = "test"
    password = getenv("PASSWORD")
    receiver = "test"

    # setup the email to be sent
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    # opens the image file
    with open(image, "rb") as file:
        content = file.read()

    # adds the attachment
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # sets up the gmail host and account
    gmail = st.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)

    # sends the email
    gmail.sendmail(username, receiver, email_message.as_string())
    # quits the smtp protocol
    gmail.quit()


if __name__ == "__main__":
    send_email(image="images/19.png")