import resend
import os
from django.urls import reverse
from django.template.loader import render_to_string

def send_verification_email(request, user):
    resend.api_key = os.getenv('RESEND_API_KEY')

    token = user.verification_token
    verify_url = request.build_absolute_uri(
        reverse('verify-email', kwargs={'token': str(token)})
    )

    html_content = render_to_string('accounts/verification_email.html', {
        'user': user,
        'verification_link': verify_url,
    })

    resend.Emails.send({
        "from": "onboarding@resend.dev",  # use this until you verify a domain
        "to": "utibefrank07@gmail.com",
        "subject": "Verify your email address",
        "html": html_content,
    })