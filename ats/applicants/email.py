from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, password):
    """ Sends a verification email to the candidate """
    print("Email: " + email)
    print("Password: " + password)
    subject = "Your Password for the JBS Applicant Portal"
    message = f"Dear {email.split('@')[0]},\n\n" \
    f"Your verification code is: {password}\n" \
    "Please use this code to log in to the JBS Applicant Portal.\n\n" \
    "Thank you,\n" \
    "JBS Applicant Portal Team\n\n" \
    "This is an automated message. Please do not reply to this email."
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)
    return True

def send_email(subject, message, from_email, to_email, fail_silently=False):
    """ Uses django send_mail to send an email"""
    send_mail(subject, message, from_email, to_email, fail_silently=fail_silently)
    return True
