from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
       
        model = CustomUser
        fields=(

            "username",
            "email",
            "phone_number",
            "role",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].choices=[
            choice 
            for choice in self.fields["role"].choices

                if choice[0] !="admin"
            ]

class LoginForm(AuthenticationForm):
    pass