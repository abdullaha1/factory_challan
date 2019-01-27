from django import forms
from master_data.models.user_profile import UserProfile
from django.contrib.auth.models import User
from master_data.controllers.register import RegisterController


class UserProfileRegistrationForm(forms.ModelForm):
    """
    This is the Form Model of User Profile Registraion.
    The model for this Form is User Profile.
    """

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=30, help_text='Required.')

    middle_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=30, help_text='Required.')

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=30, help_text='Required.')
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=30, help_text='Required.')
    company_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=30, help_text='Required.')
    company_url = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=30, help_text='Required.')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = UserProfile
        exclude = [
            'user',
            'token',
            'deleted',
            'company',
            'middle_name',
            'created_by',
            'updated_by',
            'external_id'
            ]

    def clean(self):
        """
        In the Clean Method, we verify the equality of Password/Confirm Password.
        """
        cleaned_data = super(UserProfileRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists!"
            )
        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )
        RegisterController.create_user(cleaned_data)
