from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(email, token_id, user_id):
    data = {
        'token_id': str(token_id),
        'user_id': user_id
    }
    message = get_template('email/confirmation_email.txt').render(data)
    send_mail(subject='Confirm your email', message=message, from_email='enesdemirtas255@gmail.com',
              recipient_list=[email], fail_silently=True)