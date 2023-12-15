# utils.py

import random
import string
#from django.core.mail import send_mail
from email.message import EmailMessage
import smtplib
from userauth.models import CustomUser


def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_otp_email(email, otp):
    print(f"Sending OTP to {email} with value {otp}")
    subject = 'Your OTP for Login'
    message = f'Your OTP to get verified in adiclub is: {otp}'
    from_email = 'akashsanthosh0010@gmail.com'  # Replace with your email
    recipient_list = [email]

    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = email  # Change this line to use a string, not a list
    msg['Subject'] = subject
    msg.set_content(message)

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login("307ed7b20b1e45", "9c12fc68c768a4")
        server.send_message(msg)



def check_otp(submitted_otp, generated_otp):
    return submitted_otp == generated_otp



def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


