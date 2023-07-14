from django.core.mail import send_mail
from django.conf import settings
def send_verification_email(email, password):
    print("Email: " + email)
    print("Password: " + password)
    subject = "Your Password for the JBS Applicant Portal"
    message = f"Dear {email.split('@')[0]},\n\n" \
    f"Your password is: {password}\n" \
    "Please use this password to log in to the JBS Applicant Portal within 30 minutes.\n\n" \
    "Thank you,\n" \
    "JBS Applicant Portal Team\n\n" \
    "This is an automated message. Please do not reply to this email."
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    try:
        send_mail(subject, message, from_email, to_email, fail_silently=False)
    except:
        raise Exception("Email failed to send.")
    return True

def send_email(subject, message, from_email, to_email, fail_silently=False):
    try:
        send_mail(subject, message, from_email, to_email, fail_silently=fail_silently)
    except:
        raise Exception("Email failed to send.")
    return True