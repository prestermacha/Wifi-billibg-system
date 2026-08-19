from accounts.models import OneTimePassword,AccountUser
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.core.mail import EmailMessage

def send_otp_to_user(email):
    subject= "One-time passcode for Email verification"
    user=AccountUser.objects.get(email=email)

    expires_at=timezone.now() +timedelta(minutes=5)
    OneTimePassword.objects.filter(user=user,).delete()
    otp_obj = OneTimePassword.objects.create(user=user, expires_at=expires_at)
    otp_code = otp_obj.generate_otp()
    print(f"Generated OTP: {otp_code}")

    current_site = "dictosmart.net"
    email_body = (
        f"Hi {user.email},\n\n"
        f"Thanks for signing up on {current_site}. Please verify your email with\n"
        f"one-time passcode: {otp_code}\n\n"
        f"This code expires at {expires_at.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    d_email = EmailMessage(
        subject=subject, body=email_body, from_email=from_email, to=[email]
    )
    d_email.send(fail_silently=True)

def resend_code_to_user(email):
    
        user = AccountUser.objects.get(email=email)

        
        OneTimePassword.objects.filter(user=user).delete()
        expires_at = timezone.now() + timedelta(minutes=5)
          
        otp_record = OneTimePassword(user=user,expires_at=expires_at)
        otp_record.save()

        
        otp_code = otp_record.generate_Otp()
        print(f"Generated OTP: {otp_code}") 
        expires_at = timezone.now() + timedelta(minutes=5)
        # Send OTP via email
        subject = 'Your New OTP for Email Verification'
        email_body =  email_body = (
         f"Hi {user.email},\n\n"
        f"Please verify your email with\n"
        f"one-time passcode: {otp_code}\n\n"
        f"This code expires at {expires_at.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
        from_email = settings.DEFAULT_FROM_EMAIL
        d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
        d_email.send(fail_silently=True) 

def send_normal_email(data):
   email=EmailMessage(
       subject=data['email_subject'],
       body=data['email_body'],
       from_email=settings.EMAIL_HOST_USER,
       to=[data['to_email']]
   )
   email.send()   
