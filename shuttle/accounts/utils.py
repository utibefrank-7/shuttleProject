from django.core.mail import send_mail,EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
import threading



def send_verification_email(request, user):
    token = user.verification_token
    verify_url = request.build_absolute_uri(
        reverse('verify-email', kwargs={'token': str( token)})
    )
    html_content = render_to_string('accounts/verification_email.html', {
        'user': user,
        'verification_link': verify_url,
    })
    # Send as HTML email
    email = EmailMultiAlternatives(
        subject='Verify your email address',
        body=f'Hi {user.username}, click this link to verify your account: {verify_url}',  # plain text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")

    thread = threading.Thread(target=email.send)
    thread.daemon = True
    thread.start()