from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from .models import Driverprofile, DriverApplication, Bus

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

        widgets={
            "username": forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
             "email": forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            "phone_number": forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            "role": forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            "password1": forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            "password2": forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }
        
        #removing admin from dropdown in the role options

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].choices=[
            choice 
            for choice in self.fields["role"].choices

                if choice[0] !="admin"
            ]
        
#creating Driver profile form 
class DriverprofileForm(forms.ModelForm):
    class Meta:
        model = Driverprofile
        fields=(
            "license_number",
            "license_upload",
            "profile_picture",
            "address",
        )


        widgets = {

            'address': forms.TextInput(attrs={
                'class':'w-full border rounded-lg p-2'
            }),

            'license_number': forms.TextInput(attrs={
                'class':'w-full border rounded-lg p-2'
            }),

            'profile_picture': forms.FileInput(attrs={
                'class':'w-full'
            }),

            'license_upload': forms.FileInput(attrs={
                'class':'w-full'
            }),
        }




class DriverApplicationForm(forms.ModelForm):
    class Meta:

       
        model =DriverApplication

        fields=[
            "experience_years",
            "reason",
        ]
    widgets = {
    'experience_years': forms.NumberInput(attrs={
        'class': 'w-full border rounded-lg p-2'
    }),
    'reason': forms.TextInput(attrs={
        'class': 'w-full border rounded-lg p-2'
    }),
}


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields=(
            "vehicle_name",
            "plate_no",
            "colour",
            "capacity",
        )
class LoginForm(AuthenticationForm):
   username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Username'
        })
    )
   password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Password'
        })
    )