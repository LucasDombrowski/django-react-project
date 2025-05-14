from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'})
        # You can add custom styling or field attributes here if needed
        # For example, to add a placeholder to the username field:
        # self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        # self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'}) 