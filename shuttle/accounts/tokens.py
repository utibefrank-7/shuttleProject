from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerifiedTokenGenerator(PasswordResetTokenGenerator):
    pass

email_verification_token =EmailVerifiedTokenGenerator()