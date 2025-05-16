from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'})
        # You can add custom styling or field attributes here if needed
        # For example, to add a placeholder to the username field:
        # self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        # self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'}) 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
        help_text="A valid email address, e.g., user@example.com"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        if 'password2' in self.fields:
            self.fields['password2'].label = "Confirm password"
            self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your password'})
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email', 'class': 'form-control'})
            self.fields['email'].help_text = "A valid email address, e.g., user@example.com"

    # If you add fields like email, you might need to override the save method
    # to include them when saving the user, or handle them in the view.
    # class Meta(UserCreationForm.Meta):
    #     fields = UserCreationForm.Meta.fields + ('email',) 